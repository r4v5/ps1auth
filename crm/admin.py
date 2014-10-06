from django.contrib import admin
from django.forms import Textarea
from django.db import models
from .models import CRMPerson, PayPal, Cash, Note, EmailRecord, EmailTemplate, EmailAttachement

class PayPalInline(admin.StackedInline):
    model = PayPal

class CashInline(admin.StackedInline):
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

class EmailRecordAdminInline(admin.TabularInline):
    model = EmailRecord
    exclude = ['message', 'reply_to_email']
    readonly_fields = ['subject', 'from_email', 'to_email', 'created_at', 'sender', 'status', ]
    can_delete = False
    extra = 0
    max_num = 0

class CRMPersonAdmin(admin.ModelAdmin):
    inlines = [
        PayPalInline,
        CashInline,
        NoteInline,
        EmailRecordAdminInline,
    ]
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['email_templates'] = EmailTemplate.objects.individual_recipient()
        return super(CRMPersonAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)
    

class EmailAttachementInline(admin.StackedInline):
    model = EmailAttachement


class EmailTemplateAdmin(admin.ModelAdmin):
    inlines = [
        EmailAttachementInline
    ]


admin.site.register(CRMPerson, CRMPersonAdmin)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
