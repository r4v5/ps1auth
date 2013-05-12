from pprint import pprint
import ldap
from django.contrib.auth.models import User, AbstractBaseUser
from django.conf import settings

class PS1Backend(object):

    def authenticate(self, username=None, password=None, **kwargs):
        if len(password) == 0:
            return None

        user = None
        try:
            ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, 'cacert.pem')
            l = ldap.initialize(settings.AD_URL)
            l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            binddn = "{0}@{1}".format(username, settings.AD_DOMAIN)
            l.simple_bind_s(binddn, password)
            # would throw if bind fails
            print('ok')

            #get user info
            filter_string ='(sAMAccountName={0})'.format(username)
            ldap_user = l.search_ext_s(settings.AD_BASEDN ,ldap.SCOPE_ONELEVEL, filterstr=filter_string)[0][1]

            # HEFTODO: use django user database for now
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                django_user = User(username=ldap_user['sAMAccountName'])
                django_user.first_name = ldap_user['name']
                django_user.last_name = ldap_user['sn']
                django_user.email = ldap_user['mail']
                django_user.password = ''
                django_user.is_staff = True
                django_user.is_active = True
                django_user.is_superuser = True
                #django_user.last_login = 
                #django_user.date_joined = 
                django_user.save()
                user = django_user
            l.unbind_s()
        except ldap.INVALID_CREDENTIALS:
            print('invalid_credentials')
            pass
        pprint(user)
        return user

    def get_user(self, user_id):
        # HEFTODO: return a PS1User
        return User.objects.get(pk=user_id)
        pass

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

class PS1User(AbstractBaseUser):

    def __init__(ldap_user):
        self.ldap_user = ldap_user

    def get_full_name(self):
        first_name = self.ldap_user['name']
        last_name = self.ldap_user['sn']
        return ("{0} {1}").format(firstname, last_name)

    def get_short_name(self):
        return self.ldap_user['name']

    def set_password(self, raw_password):
        pass

    def check_password(self, raw_password):
        pass

    def set_unusable_password(self):
        pass

    def has_usable_password(self):
        pass
