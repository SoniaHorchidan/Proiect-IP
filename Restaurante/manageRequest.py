from Restaurante.MachineLearning import RestaurantRecommender
import sys
import os
import django
path = os.path.realpath(__file__)
path = path.split('/')
path.pop()
path.pop()
path = '/'.join(path)
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE']='ProiectIP.settings'
django.setup()

from Restaurante.models import Restaurant, Keyword, Profile
from django.contrib.auth.models import User
import requests
import numpy as np

class RequestsManager:
	def __init__(self, user_id):
		self.all_preferences = self.__get_all_preferences()
		self.user_profile = self.__get_user_profile(user_id)
		self.user_id = user_id

	def __get_user_profile(self, user_id):
		user = User.objects.filter(id__in=[user_id])[0]
		return Profile.objects.filter(user__in=[user])[0]

	def __get_all_users(self):
		users = User.objects.all()
		users = [el.id for el in users]
		return users

	def __get_all_preferences(self):
		all_preferences = list(Keyword.objects.all())
		all_preferences = [el.id for el in all_preferences]
		return all_preferences

	def __get_user_info(self):
		return self.user_profile.trained

	def __add_artificial_id(self):
		self.user_profile.trained = True
		self.user_profile.save()

	def manage(self, list_of_restaurants):
		# takes a list of restaurants(by name) around the user and the user ID(current user)
		# gets all the needed data from database
		# passes the information to the restaurant recommender
		recommender = RestaurantRecommender()
		recommender.load_model()
		trained = self.__get_user_info()
		result, trained = recommender.predict(user_features=self.__get_user_preferences(),
									items_features=self.__get_restaurants_preferences(),
									restaurants_around=self.__get_restaurants_around(list_of_restaurants),
									trained_user=trained,
									restaurants_min_id=self.min)
		if (not trained):
			self.__add_artificial_id()

		return self.__get_coordinates(result)

	def __get_coordinates(self, list_of_restaurants):
		coordinates = Restaurant.objects.filter(id__in=list_of_restaurants)

		for el in coordinates:
			print(el.name)
		
		coordinates = [el.location for el in coordinates]
		return coordinates

	def __get_restaurants_around(self, list_of_restaurants):
		restaurants_around = Restaurant.objects.filter(name__in=list_of_restaurants)
		restaurants_around = [el.id for el in restaurants_around]
		return restaurants_around

	def __get_user_preferences(self):
		user_prefecences = self.user_profile.preferences.all()
		user_prefecences = [el.id for el in user_prefecences]
		user_prefecences = [1 if el in user_prefecences else 0 for el in self.all_preferences]
		return np.matrix(user_prefecences)

	def __get_restaurants_preferences(self):
		restaurants_features = list(Restaurant.objects.all())
		self.min = restaurants_features[0].id

		for el in restaurants_features:
			if (el.id < self.min):
				self.min = el.id

		restaurants_features = [el.keywords.all() for el in restaurants_features]
		to_return = []
		for el in restaurants_features:
			ids = [e.id for e in el]
			to_return.append([1 if e in ids else 0 for e in self.all_preferences])

		return to_return
