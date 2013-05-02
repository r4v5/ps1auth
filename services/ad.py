

class SambaBackend(object):
    def authenticate(self, username=None, password=None):
        pass

    def has_perm(self, user_obj, perm, obj=None):
        pass

    def get_user(self, user_id)
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
