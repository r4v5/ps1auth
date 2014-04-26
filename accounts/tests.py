"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from .models import PS1User
from django.test import TestCase


class AccountTest(TestCase):
    
    def test_create(self):
        user = PS1User.objects.create_user("testuser", password="Garbage1",  email="foo@bar.com")
        #self.assertEqual(user.email, "foo@bar.com")
        self.assertEqual(user.get_short_name(), 'testuser')
        self.assertTrue(user.has_usable_password())
        self.assertTrue(user.check_password('Garbage1'))
        self.assertFalse(user.check_password('wrong_password'))
        PS1User.objects.delete_user(user)
        