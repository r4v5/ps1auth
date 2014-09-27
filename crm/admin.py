from django.contrib import admin
from django.forms import Textarea
from django.db import models
from .models import CRMPerson, PayPal, Cash, Note

#Register your models here.
#admin.site.register(CRMPerson)
#admin.site.register(PayPal)
#admin.site.register(Cash)

class PayPalInline(admin.TabularInline):
    model = PayPal

class CashInline(admin.TabularInline):
    model = Cash

class NoteInline(admin.StackedInline):
    model = Note
    extra = 1
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 5})
        }
    }
    save_on_top = True

class CRMPersonAdmin(admin.ModelAdmin):
    inlines = [
        PayPalInline,
        CashInline,
        NoteInline,
    ]

admin.site.register(CRMPerson, CRMPersonAdmin)

