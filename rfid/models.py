from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class Resource(models.Model):
    name = models.CharField(max_length=160)

    def is_allowed(Tag):
        """ The default implementation just returns if the user is valid or not
        """
        key = Key.objects.get(tag)
        if key:
            return True
        else:
            return False


class RFIDNumber(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    number = models.BigIntegerField(unique=True)

    def __unicode__(self):
        return u'user={}, number={}'.format(self.user, self.number)

