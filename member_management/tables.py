import django_tables2 as tables
from django_tables2.utils import A
from .models import Person

class PersonTable(tables.Table):
    first_name = tables.LinkColumn('member_management.views.person_detail', kwargs={'person_id': A('pk')})
    last_name = tables.LinkColumn('member_management.views.person_detail', kwargs={'person_id': A('pk')})
    paypal = tables.Column(verbose_name='PayPal Email', accessor='paypal.email')
    class Meta:
        model = Person
        fields = (
            'user',
            'last_name',
            'first_name',
            'email',
            'paypal',
            'membership_status',
            'updated_on'
        )
