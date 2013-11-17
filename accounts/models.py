from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from backends import PS1Backend, get_ldap_connection
import ldap
from django.conf import settings
import uuid
from django.core.cache import cache

class PS1UserManager(BaseUserManager):
        
    def create_user(self, username, email, password):
        pass

    def create_superuser(self, username, email, password):
        self.create_user(username, email, password)

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
        first_name = self.ldap_user['givenName'][0]
        last_name = self.ldap_user['sn'][0]
        return ("{0} {1}").format(first_name, last_name)

    def get_short_name(self):
        return self.ldap_user['cn'][0]

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
        #HEFTODO fix
        return True


    #HEFTODO read source of PermissionsMixin, it might have a good default
    # implementation
    @property
    def is_staff(self):
        #HEFTODO fix this
        return True

    @property
    def is_superuser(self):
        #HEFTODO fix this
        return True

    def has_perm(self, perm, obj=None):
        #HEFTODO fix this
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
            self._ldap_user = result[0][1]
            cache.set(self.object_guid, self._ldap_user, 24 * 60 * 60)
        return self._ldap_user

def gen_uuid():
    return str(uuid.uuid4())

class Token(models.Model):
    user = models.ForeignKey('PS1User')
    key = models.CharField(max_length=36, default=gen_uuid, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)



