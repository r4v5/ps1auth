from django.db import models
from django.db.models import Sum
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
        agg = self.point_transactions.aggregate(Sum('points'))
        return agg['points__sum']

    @property
    def entries(self):
        """
        Return the queryset of point transactions for this account.
        """
        return self.point_transactions.all().order_by('-date',)

    def __unicode__(self):
        return '{}: {}'.format(self.user, self.balance)

class PointTransaction(models.Model):
    account = models.ForeignKey(PointAccount,
            related_name='point_transactions', null=False, blank=False)
    points = models.IntegerField(default=0)
    reason = models.CharField(max_length=512,
            help_text="Reason the points were added or deducted.")
    date = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
            related_name='created_point_transactions', null=False,
            blank=False)

    def __unicode__(self):
        return 'User={}, Date={}, Points={}, Reason={}'.format(
                self.account.user, self.date, self.points, self.reason)


