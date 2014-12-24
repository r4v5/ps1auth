from django.db import models, transaction
from django.conf import settings
from datetime import datetime
from django.utils import timezone
import reversion

class MemberPointManager(models.Manager):
    use_for_related_fields = True
    
    def valid(self):
        now = timezone.now()
        last_year = now.replace(now.year -1)
        return self.get_queryset().filter(created_on__gte=last_year).filter(consumed_on=None)

    def consumed(self):
        return self.get_queryset().filter(consumed_on__isnull=False)

    def expired(self):
        now = timezone.now()
        last_year = now.replace(now.year -1)
        return self.get_queryset().filter(created_on__lte=last_year)

    def next_to_expire(self):
        return self.valid().order_by('created_on')[0]

@reversion.register
class MemberPoint(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    reason = models.TextField( help_text="Reason the point was created")
    created_on = models.DateTimeField(auto_now_add=True)
    consumed_on = models.DateTimeField(null=True, blank=True)
    objects = MemberPointManager()

    def __unicode__(self):
        return u'MemberPoint({}, {}, {}, {})'.format(
            self.owner,
            self.reason,
            self.created_on,
            self.consumed_on,
        )

    def consume(self):
        with transaction.atomic(), reversion.create_revision():
            self.consumed_on = timezone.now()
            self.save()


