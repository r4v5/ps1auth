"""
Test zoho integration functionality
"""

from django.test import TestCase
from .models import Contact, Token
from datetime import datetime
from .forms import activate_account_form, account_register_form
import pytz
from accounts.models import PS1UserManager


class SimpleTest(TestCase):
    def test_activation(self):
        """
        This tests most of the zoho activation path.
        """
        c = Contact(
                    contact_id="1",
                    first_name = "Jay",
                    last_name="Hacker",
                    email="J.R.Hacker@example.com",
                    membership_status="Starving",
                    modified_time=datetime.now(pytz.UTC)
                    )
        c.save()
        activation_data = {}
        activation_data['ps1_email'] = "J.R.Hacker@example.com"
        activation_form = activate_account_form(data = activation_data)
        self.assertTrue(activation_form.is_valid())
        activation_form.save(use_https = False, domain = "example.com")
        
        #an email gets sent out. since I don't know how to retrieve it, I am going to cheat
        token = Token.objects.get(zoho_contact = c);
        self.assertIsNotNone(token)
        
        
        register_data = {}
        register_data['token'] = token.token
        register_data['preferred_username'] = 'jrhacker'
        register_data['first_name'] = 'Jay'
        register_data['last_name'] = 'Hacker'
        register_data['preferred_email'] = 'J.R.Hacker@example.com'
        register_form = account_register_form(data=register_data)
        self.assertTrue(register_form.is_valid())
        user = register_form.save()
        self.assertIsNotNone(user)
        
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(zoho_contact = c)
        
        PS1UserManager().delete_user(user)
        
        
        
        
        
