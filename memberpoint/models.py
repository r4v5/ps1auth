from django.db import models
from django.conf import settings

from datetime import datetime

class PointAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
            related_name='member_point')

    @property
    def balance(self):
        """
        The point balance of this account.
        """
        if not getattr(self, '_balance', None):
            balance = 0
            for entry in self.entries:
                balance += entry.points
            self._balance = balance
        return self._balance

    @property
    def entries(self):
        """
        Return the queryset of point transactions for this account.
        """
        return self.transaction.all().order_by('-date',)

    def __unicode__(self):
        return u'{}: {}'.format(self.user, self.balance)

class PointTransaction(models.Model):
    account = models.ForeignKey(PointAccount,
            related_name='transaction', null=False, blank=False)
    date = models.DateTimeField(default=datetime.now)
    points = models.IntegerField(default=0)
    reason = models.CharField(max_length=512,
            help_text="Reason the points were added or deducted.")

    def __unicode__(self):
        return u'User={}, Date={}, Points={}, Reason={}'.format(
                self.account.user, self.date, self.points, self.reason)


