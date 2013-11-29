from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Resource(models.Model):
    name = models.CharField(max_length=160)

    def is_allowed(self, tag):
        """ The default implementation just returns if the user is valid or not
        """

        try:
            RFIDNumber.objects.get(pk=tag.pk)
            return True
        except RFIDNumber.DoesNotExist:
            return False

    def __unicode__(self):
        return self.name


class RFIDNumber(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    number = models.BigIntegerField(unique=True)

    def __unicode__(self):
        return u'user={}, number={}'.format(self.user, self.number)

