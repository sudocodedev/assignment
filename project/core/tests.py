from django.test import TestCase
from django.contrib.auth.models import User

class UserAccountCreation(TestCase):

    def test_user_creation_failed_signal(self):

        self.assertEqual(User.objects.filter(username="TestUser_1234").exists(), False)

        with self.assertRaises(Exception):
            User.objects.create(username="TestUser_1234", email='testuser@example.com', password='Test@1234')

        self.assertEqual(User.objects.filter(username="TestUser_1234").exists(), False)

