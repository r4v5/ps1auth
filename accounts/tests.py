"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from .models import PS1User
from django.test import TestCase


class AccountTest(TestCase):
    
    def test_create_user(self):
        user = PS1User.objects.create_user("testuser", password="Garbage1",  email="foo@bar.com")
        self.assertEqual(user.get_short_name(), 'testuser')
        self.assertTrue(user.has_usable_password())
        self.assertTrue(user.check_password('Garbage1'))
        self.assertFalse(user.check_password('wrong_password'))
        PS1User.objects.delete_user(user)
        
    def test_create_superuser(self):
        user = PS1User.objects.create_superuser("superuser", email='super@user.com', password='Garbage2')
        self.assertTrue(user.is_superuser)
        PS1User.objects.delete_user(user)
        