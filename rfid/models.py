from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings


class Resource(models.Model):
    name = models.CharField(max_length=160)

    def is_allowed(self, tag):
        """
        The default implementation just returns if the user is valid or not
        """

        try:
            rfid = RFIDNumber.objects.get(pk=tag.pk)
            return rfid.user.is_active()
        except RFIDNumber.DoesNotExist:
            return False

    def __unicode__(self):
        return self.name

class AdGroupResource(Resource):
    """
    Resource that matches against AD groups.
    """
    ad_group = models.CharField(max_length=255)

    def is_allowed(self, tag):
        try:
            return tag.user.is_active() and self.ad_group in self.ldap_user['memberOf']
        except KeyError:
            return False

class RFIDNumber(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    number = models.BigIntegerField(unique=True)

    def __unicode__(self):
        return u'user={}, number={}'.format(self.user, self.number)

