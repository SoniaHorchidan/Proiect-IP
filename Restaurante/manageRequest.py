from Restaurante.MachineLearning import RestaurantRecommender
import sys
import os
import django
sys.path.append('/home/daneel/Desktop/Proiect IP/Proiect-IP')
os.environ['DJANGO_SETTINGS_MODULE']='ProiectIP.settings'
django.setup()
# merge magia
from Restaurante.models import Restaurant, Keyword, Profile
from django.contrib.auth.models import User
import requests
import numpy as np

class RequestsManager:
	def __init__(self):
		self.all_preferences = self.__get_all_preferences()

	# just for test
	def train_mock(self):

		recommender = RestaurantRecommender()
		all_preferences = self.__get_all_preferences()
		all_users = self.__get_all_users()
		users_profiles = Profile.objects.filter(user__in=all_users)
		users_preferences = [el.preferences.all() for el in users_profiles]
		all_users_preferences = []
		for el in users_preferences:
			ids = [e.id for e in el]
			all_users_preferences.append([1 if e in ids else 0 for e in all_preferences])

		all_users_preferences = np.matrix(all_users_preferences)
		print(len(all_users_preferences))
		print('-----------------')


		recommender.train(all_users_preferences, self.__get_restaurants_preferences())
		recommender.save_model()

	def __get_all_users(self):
		users = User.objects.all()
		users = [el.id for el in users]
		return users

	def __get_all_preferences(self):
		all_preferences = list(Keyword.objects.all())
		all_preferences = [el.id for el in all_preferences]
		return all_preferences

	def __get_user_info(self, user_id):
		user = User.objects.filter(id__in=[user_id])[0]
		user_profile = Profile.objects.filter(user__in=[user])[0]
		return user_profile.trained, user_profile.artificial_id

	def __add_artificial_id(self, user_id, id):
		user = User.objects.filter(id__in=[user_id])[0]
		user_profile = Profile.objects.filter(user__in=[user])[0]
		user_profile.trained = True
		user_profile.artificial_id = id
		user_profile.save()

	def manage(self, list_of_restaurants, user_id = None):
		# takes a list of restaurants(by name) around the user and the user ID(current user)
		# gets all the needed data from database
		# passes the information to the restaurant recommender
		recommender = RestaurantRecommender()
		recommender.load_model()
		trained, artificial_id = self.__get_user_info(user_id)
		result, usr = recommender.predict(user_features=self.__get_user_preferences(user_id),
									items_features=self.__get_restaurants_preferences(),
									restaurants_around=self.__get_restaurants_around(list_of_restaurants),
									user_id=artificial_id,
									trained_user=trained)
		if (usr != -1):
			self.__add_artificial_id(user_id, usr)

		return self.__get_coordinates(result)

	def __get_coordinates(self, list_of_restaurants):
		coordinates = Restaurant.objects.filter(id__in=list_of_restaurants)
		coordinates = [el.location for el in coordinates]
		return coordinates

	def __get_restaurants_around(self, list_of_restaurants):
		restaurants_around = Restaurant.objects.filter(name__in=list_of_restaurants)
		restaurants_around = [el.id for el in restaurants_around]
		return restaurants_around

	def __get_user_preferences(self, user_id):
		user = User.objects.filter(id__in=[user_id])[0]
		user_profile = Profile.objects.filter(user__in=[user])[0]
		user_prefecences = user_profile.preferences.all()
		user_prefecences = [el.id for el in user_prefecences]
		user_prefecences = [1 if el in user_prefecences else 0 for el in self.all_preferences]
		return np.matrix(user_prefecences)

	def __get_restaurants_preferences(self):
		restaurants_features = list(Restaurant.objects.all())
		restaurants_features = [el.keywords.all() for el in restaurants_features]
		to_return = []
		for el in restaurants_features:
			ids = [e.id for e in el]
			to_return.append([1 if e in ids else 0 for e in self.all_preferences])

		return to_return

# m = RequestsManager()
# m.manage(['Restaurant1', 'Restaurant3', 'Restaurant2'], 25)
#m.train_mock()

