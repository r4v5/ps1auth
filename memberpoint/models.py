from django.db import models
from django.conf import settings

from datetime import datetime

class PointAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return u'User={}'.format(self.user)

class PointTransaction(models.Model):
    account = models.ForeignKey(PointAccount,
            related_name='transaction', null=False, blank=False)
    date = models.DateTimeField(default=datetime.now)
    points = models.IntegerField(default=0)
    reason = models.TextField(max_length=512,
            help_text="Reason the points were added or deducted.")

    def __unicode__(self):
        return u'User={}, Date={}, Points={}, Reason={}'.format(
                self.account.user, self.date, self.points, self.reason)


