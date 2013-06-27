from zoho_integration.zoho import ZohoClient
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        zc = ZohoClient()
        zc.update_database()
