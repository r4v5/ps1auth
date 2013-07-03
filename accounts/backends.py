from pprint import pprint
import ldap
from django.contrib.auth.models import User, BaseUserManager
from django.conf import settings
import base64
import models


def get_ldap_connection( binddn=settings.AD_BINDDN, password=settings.AD_BINDDN_PASSWORD):
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
    l = ldap.initialize(settings.AD_URL)
    l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
   # try:
    l.simple_bind_s(binddn, password)
    return l
    #except ldap.INVALID_CREDENTIALS:
    #    return None

class PS1Backend(object):

    def authenticate(self, username=None, password=None, **kwargs):
        if len(password) == 0:
            return None

        user = None
        try:
            #ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, 'cacert.pem')
            # HEFTODO re enable strict checking
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
            l = ldap.initialize(settings.AD_URL)
            l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            binddn = "{0}@{1}".format(username, settings.AD_DOMAIN)
            l.simple_bind_s(binddn, password)
            # would throw if bind fails

            #get user info
            filter_string ='(sAMAccountName={0})'.format(username)
            ldap_user = l.search_ext_s(settings.AD_BASEDN ,ldap.SCOPE_ONELEVEL, filterstr=filter_string)[0][1]
            search_guid = ''.join('\\%02x' % ord(x) for x in ldap_user['objectGUID'][0])
            try:
                user = models.PS1User.objects.get(object_guid=search_guid)
                user.ldap_user = ldap_user
            except models.PS1User.DoesNotExist:
                django_user = models.PS1User(object_guid=search_guid)
                django_user.ldap_user = ldap_user
                django_user.save()
                user = django_user
            l.unbind_s()
        except ldap.INVALID_CREDENTIALS:
            pass
        return user

    def get_user(self, user_id):
        user = models.PS1User.objects.get(object_guid=user_id)
        l = get_ldap_connection()
        filter_string = r'(objectGUID={0})'.format(user_id)
        result = l.search_ext_s(settings.AD_BASEDN, ldap.SCOPE_ONELEVEL, filterstr=filter_string)
        user.ldap_user = result[0][1]
        return user

    def get_group_permissions(self, user_obj, obj=None):
        pprint(user_ob)
        pass

    def get_all_permissions(self, user_obj, obj=None):
        pprint(user_ob)
        pass

    def has_perm(self, user_obj, perm, obj=None):
        pprint(user_ob)
        print(perm)
        pass

    def has_module_perms(self, user_obj, app_label):
        print("has_module_perms({0} {1})".format(user_obj, app_label))

