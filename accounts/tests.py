from django.test import TestCase
from .models import PS1User
from ldap3 import Server, Connection, SUBTREE, Tls, MODIFY_REPLACE, BASE, ALL_ATTRIBUTES
from django.conf import settings
from pprint import pprint
import uuid


class AccountTest(TestCase):

    def setUp(self):
        tls = Tls()
        server = Server(settings.AD_URL, tls=tls)
        self.connection = Connection(server, user=settings.AD_BINDDN, password=settings.AD_BINDDN_PASSWORD, auto_bind=True)
        with self.connection as c:
            c.search(settings.AD_BASEDN, '(objectClass=user)', SUBTREE, attributes = ['sAMAccountName', 'objectGUID', 'userAccountControl'])
            response = c.response
            result =c.result

#        with self.connection as c:
#            c.delete('cn=testuser,{}'.format(settings.AD_BASEDN))

    def skip_test_create_user_assumption(self):
        username = 'assume'
        first_name = 'test'
        last_name = 'user'
        email = 'testuser@example.com'

        dn = "CN={0},{1}".format(username, settings.AD_BASEDN)
        object_class = ['top', 'person', 'organizationalPerson', 'user']
        attributes = {
            'cn':  username,
            'userPrincipalName': username + '@' + settings.AD_DOMAIN,
            'sAMAccountName': username,
            'userAccountControl': '514'
        }

        # Our forms will always define these, but django gets unhappy if you require
        # more than a username and password
        if first_name:
            attributes['givenName'] = first_name
        if last_name:
            attributes['sn'] = last_name
        if email:
            attributes['mail'] = email

        with self.connection as c:
            c.add(dn, object_class, attributes)
            response = c.response
            result = c.result

        with self.connection as c:
            c.search(dn, '(objectClass=*)', BASE, attributes=['objectGUID'])
            response = c.response
            result = c.result
        guid_bytes = response[0]['attributes']['objectGUID'][0]
        guid = uuid.UUID(bytes_le=guid_bytes)

        changes = {
                'userAccountControl': (MODIFY_REPLACE, ['512'])
        }

        with self.connection as c:
            c.modify(dn, changes)
            response = c.response
            result = c.result

        with self.connection as c:
            c.delete(dn)
            response = c.response
            result = c.result

    def test_create_user(self):
        user = PS1User.objects.create_user("testuser", password="Garbage1",  email="foo@bar.com")
        self.assertEqual(user.get_short_name(), 'testuser')
        self.assertTrue(user.has_usable_password())
        self.assertTrue(user.check_password('Garbage1'))
        self.assertFalse(user.check_password('wrong_password'))
        self.assertEqual("foo@bar.com", user.ldap_user['mail'][0])
        PS1User.objects.delete_user(user)

    def skip_test_create_superuser(self):
        user = PS1User.objects.create_superuser("superuser", email='super@user.com', password='Garbage2')
        self.assertTrue(user.is_superuser)
        #PS1User.objects.delete_user(user)


class TestPage(TestCase):
    def setIp(self):
        pass
    def test_page_loads(self):
        pass
