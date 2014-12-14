from django.contrib import admin
from .models import MemberPoint
import reversion

class MemberPointAdmin(reversion.VersionAdmin):
    pass

admin.site.register(MemberPoint, MemberPointAdmin)

