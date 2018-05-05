from MachineLearning import RestaurantRecommender
import numpy as np
import random
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
from Restaurante.models import Restaurant



NUMBER_OF_KEYWORDS = 5
NUMBER_OF_USERS = 100000;
KEYWORDS = ['Burger', 'Romanian', 'Pasta', 'Pizza', 'Soup', 'Salad',
			'Meat', 'Vegan', 'Greek', 'Italian', 'Libanese', 'Sushi', 'Chinese', 
			'Asian', 'Indian', 'Shawarma', 'BBQ', 'Sandwich', 'Dessert', 'Scrambled Eggs',
			'Fish']


def generate_user():
	features = random.sample(range(0, len(KEYWORDS)), NUMBER_OF_KEYWORDS)
	features = [1 if i in features else 0 for i in range(len(KEYWORDS))]
	return features	

def generate_all_users():
	users_features = []

	for _ in range(NUMBER_OF_USERS):
		users_features.append(generate_user())

	return np.matrix(users_features)

def get_restaurants_preferences():
	restaurants_features = list(Restaurant.objects.all())
	restaurants_features = [el.keywords.all() for el in restaurants_features]
	to_return = []

	for el in restaurants_features:
		names = [e.name for e in el]
		to_return.append([1 if e in names else 0 for e in KEYWORDS])

	return to_return

if __name__=="__main__":
	recommender = RestaurantRecommender()
	recommender.train(generate_all_users(), get_restaurants_preferences())
	recommender.save_model()
	#recommender.save_number_of_users(NUMBER_OF_USERS - 1)