from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here

class PS1UserManager(BaseUserManager):
        
    def create_user(self, username, email, password):
        pass

    def create_superuser(self, username, email, password):
        self.create_user(username, email, password)

class PS1User(AbstractBaseUser):

    objects = PS1UserManager()
    sAMAccountName = models.EmailField(verbose_name='Username',
            max_length=255,
            unique=True,
            db_index=True,
            )
    USERNAME_FIELD = 'sAMAccountName'

    def get_full_name(self):
        first_name = self.ldap_user['name']
        last_name = self.ldap_user['sn']
        return ("{0} {1}").format(firstname, last_name)

    def get_short_name(self):
        return self.ldap_user['name']

    def check_password(self, raw_password):
        # HEFTODO strict check
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
        l = ldap.initialize(settings.AD_URL)
        l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        binddn = "{0}@{1}".format(self.username,  settings.AD_DOMAIN)
        try:
            l.simple_bind_s(binddn, password)
            return True
        except ldap.INVALID_CREDENTIALS:
            return False

    def set_password(self, raw_password):
        """" HEFTODO: would prefer a non admin override
        That means we need the current password and the new password.
        Requiring those means that the change password form needs some
        rework."""
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT,ldap.OPT_X_TLS_ALLOW)
        l = ldap.initialize(settings.AD_URL)
        l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        binddn = "{0}@{1}".format(settings.AD_BINDDN, settings.AD_DOMAIN)
        l.simple_bind_s(binddn, settings.AD_BINDDN_PASSWORD)
        unicode_pass = unicode('"' + password + '"', 'iso-8859-1')
        password_value = unicode_pass.centerencode('utf-16-le')
        add_pass = [(ldap.MOD_REPLACE, 'unicodePwd', [password_value])]
       
        user_dn = self.ldap_user['distinguishedName'][0]
        ldap_connection.modify_s(user_dn, add_pass)
        print("password changed")
        
    def set_unusable_password(self):
        pass

    def has_usable_password(self):
        pass
