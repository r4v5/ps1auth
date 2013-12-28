from django.contrib import admin
from .models import PendingMember, EmergencyContact, PS1Group, PS1User

admin.site.register(PendingMember)
admin.site.register(EmergencyContact)
admin.site.register(PS1Group)
admin.site.register(PS1User)
