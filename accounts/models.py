from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import backends
import ldap
from django.conf import settings
import uuid

class PS1UserManager(BaseUserManager):
        
    def create_user(self, username, email, password):
        pass

    def create_superuser(self, username, email, password):
        self.create_user(username, email, password)

    def get_users_by_field(self, field, value):
        l = backends.get_ldap_connection()
        filter_string = "({0}={1})".format(field, value)
        #HEFTODO build user result directly
        result = l.search_s(settings.AD_BASEDN, ldap.SCOPE_ONELEVEL, filterstr=filter_string)
        backend = backends.PS1Backend()
        users = []
        for ldap_user in result:
            guid = uuid.UUID(bytes_le=(ldap_user[1]['objectGUID'][0]))
            users.append(backend.get_user(str(guid)))
        return users


class PS1User(AbstractBaseUser):
    """ Represents a User
        TODO: add an ldapobject property
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
        first_name = self.ldap_user['name'][0]
        last_name = self.ldap_user['sn'][0]
        return ("{0} {1}").format(first_name, last_name)

    def get_short_name(self):
        return self.ldap_user['name'][0]

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
        l = backends.get_ldap_connection()
        #unicode_pass = unicode('"' + raw_password + '"', 'iso-8859-1')
        unicode_pass = '"' + raw_password + '"'
        password_value = unicode_pass.encode('utf-16-le')
        add_pass = [(ldap.MOD_REPLACE, 'unicodePwd', [password_value])]
        user_dn = self.ldap_user['distinguishedName'][0]
        l.modify_s(user_dn, add_pass)
        
    def set_unusable_password(self):
        raise NotImplementedError

    def has_usable_password(self):
        raise NotImplementedError


def gen_uuid():
    return str(uuid.uuid4())

class Token(models.Model):
    user = models.ForeignKey('PS1User')
    key = models.CharField(max_length=36, default=gen_uuid, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)



