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

class RegisterTest(TestCase):
	def setUp(self):
		k = Keyword(name='Burger')
		k.save(force_insert=True)
		k = Keyword(name='Salad')
		k.save(force_insert=True)
		k = Keyword(name='Pizza')
		k.save(force_insert=True)

		self.query = Keyword.objects.all()
		
		self.data = {
				'username': 'testest',
				'password1': 'parola12345',
				'password2': 'parola12345',
				'email': 'test@gmail.com',
				'first_name': 'Test',
				'last_name': 'Test',
				'birth_date': '02/02/1990',
				'preferences': self.query
		}

	def test_registration_view_get(self):
		response = self.client.get(reverse('signup'))
		self.assertEqual(response.status_code, 200)

	def test_registration(self):
		form = SignUpForm(data=self.data)
		self.assertTrue(form.is_valid(), 'Form is not valid')