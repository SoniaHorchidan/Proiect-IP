from MachineLearning import RestaurantRecommender
from keywordFinder import findKeywords
# aplicam magie
import sys
import os
import django
sys.path.append('/home/daneel/Desktop/Proiect IP/Proiect-IP')
os.environ['DJANGO_SETTINGS_MODULE']='ProiectIP.settings'
django.setup()
# merge magia
from Restaurante.models import Restaurant
import requests
# import os
# import sys
# sys.path.append('/path/to/the/directory/above/your/project')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'yourproject.settings'
# from  yourproject.yourapp.models import YourModel




# AIzaSyA3vy2oO5XSTevGLcfja_R9EPcDzV89UdE

def add_restaurant(restaurant):
	r = Restaurant(name=restaurant["name"], rating=restaurant["rating"], 
		location=restaurant["location"], website=restaurant["website"])
	r.save(force_insert=True)

def get_restaurants_in_Bucharest():
	latitude = 0
	longitude = 0
	url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=44.439663,26.096306&radius=10000&type=restaurant&key=AIzaSyA3vy2oO5XSTevGLcfja_R9EPcDzV89UdE"
	response = requests.get(url)
	response = response.json()["results"]

	to_return = []

	for el in response:
		lat = el["geometry"]["location"]["lat"]
		lng = el["geometry"]["location"]["lng"]
		location = str(lat) + "T" + str(lng)
		rating = el["rating"]
		name = el["name"]
		place_id = el["place_id"]	
		url2 = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + "&key=AIzaSyA3vy2oO5XSTevGLcfja_R9EPcDzV89UdE"
		response2 = requests.get(url2)
		website = response2.json()["result"]["website"]

		new_dict = dict()
		new_dict["name"] = name
		new_dict["rating"] = float(rating)
		new_dict["location"] = location
		new_dict["website"] = website
		to_return.append(new_dict)

	print("AAA")
	add_restaurant(to_return[0])


if __name__ == "__main__":
	get_restaurants_in_Bucharest()