from datetime import datetime
from django.test import TestCase
import pytz

from accounts.models import PS1User
from member_management.models import Person

from .forms import activate_account_form, account_register_form
from .models import Token


class SimpleTest(TestCase):
    def test_activation(self):
        """
        This tests most of the zoho activation path.
        """
        c = Person(
                    first_name = "Jay",
                    last_name="Hacker",
                    email="J.R.Hacker@example.com",
                    membership_status="Starving",
                    )
        c.save()
        activation_data = {}
        activation_data['ps1_email'] = "J.R.Hacker@example.com"
        activation_form = activate_account_form(data = activation_data)
        self.assertTrue(activation_form.is_valid())
        activation_form.save(use_https = False, domain = "example.com")
        
        #an email gets sent out. since I don't know how to retrieve it, I am going to cheat
        token = Token.objects.get(person = c);
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
            Token.objects.get(person = c)
        
        PS1User.objects.delete_user(user)

        
