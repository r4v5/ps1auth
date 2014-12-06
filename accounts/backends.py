import ldap3
from django.contrib.auth.models import User, BaseUserManager
from django.conf import settings
import base64
import uuid


def get_ldap_connection( binddn=settings.AD_BINDDN, password=settings.AD_BINDDN_PASSWORD):
    ldap3.set_option(ldap3.OPT_X_TLS_REQUIRE_CERT, ldap3.OPT_X_TLS_ALLOW)
    l = ldap3.initialize(settings.AD_URL)
    l.set_option(ldap3.OPT_PROTOCOL_VERSION, 3)
    l.simple_bind_s(binddn, password)
    return l

class PS1Backend(object):

    def authenticate(self, username=None, password=None, **kwargs):
        if len(password) == 0:
            return None

        user = None
        try:
            #ldap3.set_option(ldap3.OPT_X_TLS_CACERTFILE, 'cacert.pem')
            # HEFTODO re enable strict checking
            ldap3.set_option(ldap3.OPT_X_TLS_REQUIRE_CERT, ldap3.OPT_X_TLS_ALLOW)
            l = ldap3.initialize(settings.AD_URL)
            l.set_option(ldap3.OPT_PROTOCOL_VERSION, 3)
            binddn = "{0}@{1}".format(username, settings.AD_DOMAIN)
            l.simple_bind_s(binddn, password)
            # would throw if bind fails

            filter_string ='(sAMAccountName={0})'.format(username)
            ldap_user = l.search_ext_s(settings.AD_BASEDN ,ldap3.SCOPE_ONELEVEL, filterstr=filter_string)[0][1]
            guid = uuid.UUID(bytes_le=ldap_user['objectGUID'][0])
            user = self.get_user(str(guid))
            l.unbind_s()
        except ldap3.INVALID_CREDENTIALS:
            # Swallow the exception and return a None object.  Django handles this gracefully
            pass
        return user

    def get_user(self, user_id):
        """
        Get's The user object and attached ldap_user data.
        Will create the database entry if required.

        Keyword arguments:
        user_id -- a string or UUID object of samba4 objectGUID of a user.
        """
        from accounts.models import PS1User
        try:
            guid = uuid.UUID(str(user_id))
        except ValueError:
            # Happens when we get passed an invalid or outdated user_id
            return None
        try:
            user = PS1User.objects.get(object_guid=str(guid))
        except PS1User.DoesNotExist:
            l = get_ldap_connection()
            # certain byte sequences contain printable character that can
            # potentially be parseable by the query string.  Escape each byte as
            # hex to make sure this doesn't happen.
            restrung = ''.join(['\\%02x' % ord(x) for x in guid.bytes_le])
            filter_string = r'(objectGUID={0})'.format(restrung)
            result = l.search_ext_s(settings.AD_BASEDN, ldap3.SCOPE_ONELEVEL, filterstr=filter_string)
            user = PS1User(object_guid=str(guid))
            user.save()
        return user

    def get_group_permissions(self, user_obj, obj=None):
        raise NotImplementedError

    def get_all_permissions(self, user_obj, obj=None):
        raise NotImplementedError

    def has_perm(self, user_obj, perm, obj=None):
        raise NotImplementedError

    def has_module_perms(self, user_obj, app_label):
        raise NotImplementedError

