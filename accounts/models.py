from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .backends import PS1Backend, get_ldap_connection
import ldap
from django.conf import settings
import uuid
from django.core.cache import cache
import ldap.modlist
from pprint import pprint

class PS1UserManager(BaseUserManager):
        
    def create_user(self, username, email = None, first_name = None, last_name = None, password = None):
        user_dn = "CN={0},{1}".format(username, settings.AD_BASEDN)
        user_attrs = {}
        user_attrs['objectClass'] = ['top', 'person', 'organizationalPerson', 'user']
        user_attrs['cn'] = username
        user_attrs['userPrincipalName'] = username + '@' + settings.AD_DOMAIN
        user_attrs['sAMAccountName'] = username
        if first_name:
            user_attrs['givenName'] = first_name
        if last_name:
            user_attrs['sn'] = last_name
        user_attrs['userAccountControl'] = '514'
        if email:
            user_attrs['mail'] = email
        user_ldif = ldap.modlist.addModlist(user_attrs)

        # prep account enable
        enable_account = [(ldap.MOD_REPLACE, 'userAccountControl', '512')]

        ldap_connection = get_ldap_connection()

        # add the user to AD
        result = ldap_connection.add_s(user_dn, user_ldif)

        #now get the user guid
        filter_string = r'sAMAccountName={0}'.format(username)
        result = ldap_connection.search_ext_s(settings.AD_BASEDN, ldap.SCOPE_ONELEVEL, filterstr=filter_string)
        ldap_user = result[0][1]
        guid = uuid.UUID(bytes_le=ldap_user['objectGUID'][0])
        user = PS1Backend().get_user(guid)
        user.save()
        
        #set password
        if password:
            user.set_password(password)
            
        #turn the account on
        result = ldap_connection.modify_s(user_dn, enable_account)
        user._expire_ldap_data()
        return user
    
    def delete_user(self, user):
        l = get_ldap_connection()
        user_dn = user.ldap_user['distinguishedName'][0]
        result = l.delete_s(user_dn)
        user.delete()
        
    def create_superuser(self, object_guid, password, email = None):
        """
        object_guid is actually a username. calling it object_guid gets around
        a bug in ./manage.py createsuperuser
        """
        user = self.create_user(object_guid, email=email, password=password)
        admins_dn = "CN={0},{1}".format("Domain Admins", settings.AD_BASEDN)
        user_dn = user.ldap_user['distinguishedName'][0]
        add_member = [(ldap.MOD_ADD, 'member', user_dn)]
        l = get_ldap_connection()
        l.modify_s(admins_dn, add_member)
        return user

    def get_users_by_field(self, field, value):
        l = get_ldap_connection()
        filter_string = "({0}={1})".format(field, value)
        #HEFTODO build user result directly
        result = l.search_s(settings.AD_BASEDN, ldap.SCOPE_ONELEVEL, filterstr=filter_string)
        backend = PS1Backend()
        users = []
        for ldap_user in result:
            guid = uuid.UUID(bytes_le=(ldap_user[1]['objectGUID'][0]))
            users.append(backend.get_user(str(guid)))
        return users


class PS1User(AbstractBaseUser):
    """ Represents a User
    """

    objects = PS1UserManager()
    object_guid = models.CharField(
            verbose_name="Username",
            max_length=48,
            primary_key=True,
            unique=True,
            db_index=True,
            editable=False,
        )
    USERNAME_FIELD = 'object_guid'

    def get_full_name(self):
	if not self.ldap_user:
	     return repr(self)
        try:
            first_name = self.ldap_user['givenName'][0]
            last_name = self.ldap_user['sn'][0]
        except KeyError:
            return repr(self)
        return ("{0} {1}").format(first_name, last_name)

    def get_short_name(self):
	if self.ldap_user:
		return self.ldap_user['cn'][0]
	else:
		return "AD User Set, but not found"

    def check_password(self, raw_password):
        # HEFTODO strict check
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
        l = ldap.initialize(settings.AD_URL)
        l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        username = self.ldap_user['sAMAccountName'][0]
        binddn = "{0}@{1}".format(username,  settings.AD_DOMAIN)
        try:
            l.simple_bind_s(binddn, raw_password)
            return True
        except ldap.INVALID_CREDENTIALS:
            return False

    def set_password(self, raw_password):
        l = get_ldap_connection()
        #unicode_pass = unicode('"' + raw_password + '"', 'iso-8859-1')
        unicode_pass = '"' + raw_password + '"'
        password_value = unicode_pass.encode('utf-16-le')
        add_pass = [(ldap.MOD_REPLACE, 'unicodePwd', [password_value])]
        user_dn = self.ldap_user['distinguishedName'][0]
        l.modify_s(user_dn, add_pass)
        
    def set_unusable_password(self):
        raise NotImplementedError

    def has_usable_password(self):
       return self.is_active

    @property
    def is_superuser(self):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm_list, obj=None):
        #HEFTODO fix this
        return True

    def has_module_perms(self, package_name):
        #HEFTODO fix this
        return True

    @property
    def is_active(self):
        return (int(self.ldap_user['userAccountControl'][0]) & 2) != 2

    @property
    def is_staff(self):
        domain_admins_dn = "CN=Domain Admins,{}".format(settings.AD_BASEDN)
        try:
            return domain_admins_dn in self.ldap_user['memberOf']
        except KeyError:
            return False

    @property
    def ldap_user(self):
        if hasattr(self, '_ldap_user'):
            return self._ldap_user
        self._ldap_user = cache.get(self.object_guid)
        if not self._ldap_user:
            guid = uuid.UUID(self.object_guid)
            # certain byte sequences contain printable character that can
            # potentially be parseable by the query string.  Escape each byte as
            # hex to make sure this doesn't happen.
            restrung = ''.join(['\\%02x' % ord(x) for x in guid.bytes_le])
            filter_string = r'(objectGUID={0})'.format(restrung)
            l = get_ldap_connection()
            result = l.search_ext_s(settings.AD_BASEDN, ldap.SCOPE_ONELEVEL, filterstr=filter_string)
            if len(result) > 0:
		    self._ldap_user = result[0][1]
		    cache.set(self.object_guid, self._ldap_user, 24 * 60 * 60)
        return self._ldap_user
    
    def _expire_ldap_data(self):
        if hasattr(self, '_ldap_user'):
            del(self._ldap_user)
        cache.delete(self.object_guid)

    def __unicode__(self):
        return self.get_short_name()

def gen_uuid():
    return str(uuid.uuid4())

class Token(models.Model):
    user = models.ForeignKey('PS1User')
    key = models.CharField(max_length=36, default=gen_uuid, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)



