from MachineLearning import RestaurantRecommender
from keywordFinder import findKeywords
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
from Restaurante.models import Restaurant, Keyword
import requests


def add_restaurant(restaurant, keywords):
	if (restaurant['name'] == 'Theater Pub Inlight'):
		return

	r = Restaurant(name=restaurant["name"], rating=restaurant["rating"], 
		location=restaurant["location"], website=restaurant["website"])

	# print(keywords)
	# return

	k = Keyword.objects.filter(name__in=keywords)
	# print(k)
	# print(k[0])
	# return
	r.save(force_insert=True)

	r = Restaurant.objects.filter(name__in=[restaurant['name']])[0]

	for el in k:
		r.keywords.add(el)
	# r.keywords.add(k)
	r.save()


def get_restaurants_in_Bucharest():
	url1 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=44.435512,26.099617&radius=1000&type=restaurant&key=AIzaSyBCopeprKdGdqxvjoX-SPxV49WD8PYhSNI"
	url2 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=44.435196,26.099722&radius=1000&type=restaurant&key=AIzaSyBCopeprKdGdqxvjoX-SPxV49WD8PYhSNI"
	url3 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=44.436028,26.101778&radius=1000&type=restaurant&key=AIzaSyBCopeprKdGdqxvjoX-SPxV49WD8PYhSNI"
	url4 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=44.435641,26.101881&radius=1000&type=restaurant&key=AIzaSyBCopeprKdGdqxvjoX-SPxV49WD8PYhSNI"
	url5 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=44.435616,26.100850&radius=1000&type=restaurant&key=AIzaSyBCopeprKdGdqxvjoX-SPxV49WD8PYhSNI"


	responses = [requests.get(url1).json()["results"], requests.get(url2).json()["results"], requests.get(url3).json()["results"],
				requests.get(url4).json()["results"], requests.get(url5).json()["results"]]
	
	#responses = [requests.get(url1).json()["results"]]
	to_return = []


	for r in responses:
		for el in r:
			lat = el["geometry"]["location"]["lat"]
			lng = el["geometry"]["location"]["lng"]
			location = str(lat) + "T" + str(lng)
			if 'rating' not in el:
				rating = 0
			else:
				rating = el["rating"]
			name = el["name"]
			place_id = el["place_id"]	
			url6 = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + "&key=AIzaSyBCopeprKdGdqxvjoX-SPxV49WD8PYhSNI"
			response2 = requests.get(url6)
			response2 = response2.json()["result"]
			if 'website' not in response2:
				website = ''
			else:
				website = response2["website"]

			new_dict = dict()
			new_dict["name"] = name
			new_dict["rating"] = float(rating)
			new_dict["location"] = location
			new_dict["website"] = website

			if (new_dict not in to_return):
				to_return.append(new_dict)


	for i in range(len(to_return)):
		print(i, to_return[i]['name'])

	keywords = []
	keywords.append(['Romanian', 'Pasta', 'Soup', 'Salad', 'Meat', 'BBQ', 'Dessert'])
	keywords.append(['Sushi', 'Dessert', 'Asian'])
	keywords.append(['Romanian', 'Burger', 'Soup', 'Salad', 'Dessert', 'Meat'])
	keywords.append(['Romanian', 'Soup', 'Burger', 'Pasta', 'Dessert', 'Scrambled Eggs'])
	keywords.append(['Romanian', 'Soup', 'Scrambled Eggs', 'Salad', 'BBQ', 'Dessert', 'Burger', 'Meat', 'Vegan', 'Fish'])
	keywords.append(['Romanian', 'Soup', 'Scrambled Eggs', 'Salad', 'BBQ', 'Dessert', 'Burger', 'Meat', 'Vegan', 'Fish'])
	keywords.append(['Salad', 'Meat', 'BBQ', 'Burger', 'Dessert'])
	keywords.append(['Pizza', 'Burger', 'Salad', 'Dessert', 'BBQ', 'Meat', 'Pasta', 'Vegan'])
	keywords.append(['Dessert', 'Soup', 'Romanian', 'Meat', 'BBQ', 'Salad'])
	keywords.append(['Soup', 'Salad', 'Dessert', 'Meat', 'BBQ'])
	keywords.append(['Italian', 'Soup', 'Pasta', 'Pizza', 'Fish'])
	keywords.append(['Meat', 'BBQ', 'Scrambled Eggs', 'Burger', 'Romanian', 'Fish', 'Salad', 'Soup', 'Pasta', 'Dessert']) 
	keywords.append(['Meat', 'BBQ', 'Soup', ])
	keywords.append([''])
	keywords.append(['Soup', 'Salad', 'Meat', 'Burger', 'Fish', 'Pasta', 'Dessert'])
	keywords.append(['Soup', 'Scrambled Eggs', 'Pasta', 'Vegan', 'Sandwich', 'Salad'])
	keywords.append(['Pizza', 'Burger', 'Pasta', 'Soup', 'Salad', 'Meat', 'Vegan', 'Dessert'])
	keywords.append(['Sandwich'])
	keywords.append(['Scrambled Eggs', 'Soup', 'Salad', 'Pasta', 'Meat', 'Fish', 'Asian', 'BBQ', 'Pizza', 'Burger', 'Sandwich', 'Dessert'])
	keywords.append(['Pasta', 'Pizza', 'Salad', 'BBQ', 'Meat', 'Soup', 'Chinese', 'Libanese'])
	keywords.append(['Soup', 'Fish', 'Dessert', 'Salad', 'Romanian', 'Meat', 'BBQ', 'Scrambled Eggs'])
	keywords.append(['Romanian', 'Sandwich', 'Salad', 'Fish', 'Dessert', 'Soup', 'Meat', 'BBQ'])

	for el, k in zip(to_return, keywords):
		add_restaurant(el, k)


def add_keywords():
	keywords = ['Burger', 'Romanian', 'Pasta', 'Pizza', 'Soup', 'Salad',
				'Meat', 'Vegan', 'Greek', 'Italian', 'Libanese', 'Sushi', 'Chinese', 
				'Asian', 'Indian', 'Shawarma', 'BBQ', 'Sandwich', 'Dessert', 'Scrambled Eggs',
				'Fish']

	for el in keywords:
		k = Keyword(name=el)
		k.save(force_insert=True)



if __name__ == "__main__":
	add_keywords()
	get_restaurants_in_Bucharest()
	pass