from django.db import models
from django.db.models import Sum
from django.conf import settings
from datetime import datetime
import reversion

@reversion.register
class MemberPoint(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    reason = models.TextField( help_text="Reason the point was created")
    created_on = models.DateTimeField(auto_now_add=True)
    consumed_on = models.DateTimeField(null=True, blank=True)
    def __unicode__(self):
        return u'MemberPoint({}, {}, {}, {})'.format(
            self.owner,
            self.reason,
            self.created_on,
            self.consumed_on,
        )


