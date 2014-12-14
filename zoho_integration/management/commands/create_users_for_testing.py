from import_zoho_scrape import zoho_user_to_ps1user_map, zoho_account_to_ps1user_map
from django.core.management.base import BaseCommand
from itertools import chain
from accounts.models import PS1User

class Command(BaseCommand):

    def handle(self, *args, **options):
        users = zoho_user_to_ps1user_map.values()
        
        more_users = [x.values() for x in zoho_account_to_ps1user_map.values()]
        needed_users = set(chain.from_iterable([chain.from_iterable(more_users),users]))
        for user in needed_users:
            users = PS1User.objects.get_users_by_field("sAMAccountName", user)
            if len(users) == 0:
                PS1User.objects.create_superuser(user, 'Password1')



