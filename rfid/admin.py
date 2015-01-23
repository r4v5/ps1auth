from django.contrib import admin
from .models import AdGroupResource, Resource, RFIDNumber

admin.site.register(Resource)
admin.site.register(RFIDNumber)
admin.site.register(AdGroupResource)
