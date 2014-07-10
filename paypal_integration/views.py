from django.shortcuts import render
from .models import Transaction
import calendar
from django.db.models import Sum, Count, Q
from django.db import connection
from moneyed import Money
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from dateutil import tz

@login_required
def reports(request):
    data = {}
    truncate_date = connection.ops.date_trunc_sql('month','timestamp - interval \'6 hours\'')
    months = Transaction.objects.extra(select={'month': truncate_date}).values('month').annotate(Count('id')).order_by('-month')
    for month in months:
        month['month'] = (month['month'] + timedelta(hours = 6 )).replace(tzinfo=tz.gettz('CST'))
    data['months'] = months 
    return render(request, 'paypal_statements.html', data)

@login_required
def report(request, year, month):
    data = {}
    data['year'] = year
    data['month'] = calendar.month_name[int(month)]

    # base query
    q = Transaction.objects.filter(timestamp__year=year, timestamp__month=month)

    # start/end balance
    first_record = q.earliest('timestamp')
    
    data['ending_balance'] = q.latest('timestamp').balance
    data['starting_balance'] = first_record.balance - first_record.net_amount
    data['payables_starting_balance'] = Money(0, 'USD')
    data['payables_ending_balance'] = Money(0, 'USD')
    data['total_starting_balance'] = data['starting_balance'] + data['payables_starting_balance']
    data['total_ending_balance'] = data['ending_balance'] + data['payables_ending_balance']

    # Payments
    received = q.filter(
            Q(type='Recurring Payment Received')|
            Q(type='Recurring Payment')|
            Q(type='Payment Received')|
            Q(type='Mobile Payment Received')|
            Q(type='Shopping Cart Payment Received')|
            Q(type='Donation Received')|
            Q(type='Recurring Payment Failed')|
            Q(type='Update to eCheck Received')| # Is a modification, counts towards current month, not month of modified record
            Q()
        ).filter(~(Q(status="Failed")&Q(fee_amount=0)))
    # Regarding Failed Transactions
    # 2013-10-20 7VN83203CL288451E: Failed Transaction we got paid on
    # 2013-07-14 00L32215R8681210S: Failed Transaction we did not get paid on (eCheck, might be special case again)
    # 2013-07-16 8F571923JM4193017: Update to 00L32215R8681210S, Status is "Updated", we still didn't get paid
    # 2012-09-15 7TX274561G349671H: Received Money, $0 fee (sender paid fee, probably)
    # The only real difference I could find was wether or not a fee was charged.

    # Regarding eChecks
    # It appears that we get an inital "payment" for echecks, but we don't actuallly get the money
    # until th e"Update to eCheck Received" comes through


    #Grab the id's of transactions that get modified as "Update to eCheck Received"
    modified_transaction_ids = Transaction.objects.filter(reference__in=received).filter(
            Q(type='Update to eCheck Received')|
            Q()
        ).values_list('reference', flat=True)

    # Find Updates to Failed Transactions (where that would invalidate the Update)
    # Might need to filter on:
    # Q(reference__status='Failed')&Q(reference__fee_amount=0)
    # or maybe: (reference__status='Failed')&Q(fee_amount=0)
    failed_update_ids = q.filter(reference__status='Failed').values_list('id', flat=True)

    # remove the modified transactions
    received = received.exclude(id__in=modified_transaction_ids)
    received = received.exclude(id__in=failed_update_ids)


    payment_sums = received.aggregate(Sum('amount'), Sum('fee_amount'))
    data['payments_received'] = payment_sums['amount__sum'] or 0
    data['disbursements_received'] = 0
    data['refunds_sent']  = q.filter(type='Refund').aggregate(Sum('amount'))['amount__sum'] or 0
    data['total_payments'] = data['payments_received'] + data['disbursements_received'] + data['refunds_sent']

    # Fees
    data['payment_fees'] = payment_sums['fee_amount__sum'] or 0
    data['refunded_fees'] = q.filter(type='Refund').aggregate(Sum('fee_amount'))['fee_amount__sum'] or 0
    data['chargeback_fees'] = 0
    data['account_fees_invoice'] = 0
    data['other_fees'] = q.filter(type='Reversal').aggregate(Sum('fee_amount'))['fee_amount__sum'] or 0
    data['total_fees'] = data['payment_fees'] + data['refunded_fees'] + data['chargeback_fees'] + data['account_fees_invoice'] + data['other_fees']

    # Disputes
    disputes = q.filter(Q(type='Reversal')|Q(type='Temporary Hold')).aggregate(Sum('amount'), Sum('net_amount'))
    dispute_reimbursements = q.filter(type='Update to Reversal').aggregate(Sum('net_amount'))
    data['chargeback_and_disputes'] = disputes['amount__sum'] or 0
    data['dispute_reimbursements'] = dispute_reimbursements['net_amount__sum'] or 0
    data['dispute_total'] = data['chargeback_and_disputes'] + data['dispute_reimbursements']

    # Transfers
    data['currency_transfers'] = 0
    data['transfer_to_paypal'] = 0
    data['transfer_from_paypal'] = q.filter(type='Withdraw Funds to a Bank Account').aggregate(Sum('net_amount'))['net_amount__sum'] or 0
    data['total_transfer'] = data['currency_transfers'] + data['transfer_to_paypal'] + data['transfer_from_paypal']

    # Purchases
    data['payments_sent'] = q.filter(
            Q(type='Payment Sent')|
            Q(type='Web Accept Payment Sent')
        ).aggregate(Sum('amount'))['amount__sum'] or 0
    data['refunds_received'] = 0 #q.filter(type='Refund').aggregate(Sum('amount'))['amount__sum'] or 0
    data['debit_card_purchases'] = 0
    data['debit_card_returns'] = 0
    data['total_purchases'] = data['payments_sent'] + data['refunds_received'] + data['debit_card_purchases'] + data['debit_card_returns']

    # Debug Table
    #data['helper_data'] = {}
    #data['helper_data']['To Pumping Station: One'] = q.filter(to_email='money@pumpingstationone.org').values('type').annotate(gross=Sum('amount'), fee=Sum('fee_amount'), net=Sum('net_amount'), count=Count('id')).order_by()
    #data['helper_data']['From Pumping Station: One'] = q.filter(from_email='money@pumpingstationone.org').values('type').annotate(gross=Sum('amount'), fee=Sum('fee_amount'), net=Sum('net_amount'), count=Count('id')).order_by()
    #data['helper_data']['Unlisted'] = q.filter(~Q(from_email='money@pumpingstationone.org')).filter(~Q(to_email='money@pumpingstationone.org')).values('type').annotate(gross=Sum('amount'), fee=Sum('fee_amount'), net=Sum('net_amount'), count=Count('id')).order_by()

    #data['debug'] = { 'modded': list(modified_transaction_ids), 'received': list(received), 'size': len(received), 'failed_updates': failed_update_ids}
    
    return render(request, 'paypal_statement.html', data)

