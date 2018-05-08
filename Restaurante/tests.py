from django.test import TestCase
from django.test import Client
from Restaurante.models import Profile, Keyword
from django.contrib.auth.models import User
from Restaurante.forms import SignUpForm

# Create your tests here.


class LoginTest(TestCase):
	def setUp(self):
		User.objects.create_user(**{'username': 'testuser1',
								  'password': 'secret'})

		User.objects.create_user(**{'username': 'testuser2',
								  'password': 'secret'})

		User.objects.create_user(**{'username': 'testuser3',
								  'password': 'secret'})

		User.objects.create_user(**{'username': 'testuser4',
								  'password': 'secret'})

		User.objects.create_user(**{'username': 'testuser5',
								  'password': 'secret'})

	def test_login(self):
		response = self.client.login(username='testuser1', password='secret')
		self.assertTrue(response)

		response = self.client.login(username='testuser2', password='secret')
		self.assertTrue(response)

		response = self.client.login(username='testuser3', password='secret')
		self.assertTrue(response)

		response = self.client.login(username='testuser4', password='secret')
		self.assertTrue(response)

		response = self.client.login(username='testuser5', password='secret')
		self.assertTrue(response)
