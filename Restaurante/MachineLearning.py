import numpy as np
from lightfm import LightFM
from scipy import sparse
import pickle
import os

class RestaurantRecommender:
	def __init__(self):
		self.model = LightFM(loss='warp')

	def train(self, users_features, items_features, epochs = 150):
		print("Training!")
		number_of_users, number_of_features = users_features.shape
		number_of_restaurants = len(items_features)
		user_ratings = np.matrix(np.zeros((number_of_users, number_of_restaurants)))
		user_ratings = sparse.coo_matrix(user_ratings)
		users_features = sparse.coo_matrix(users_features)
		items_features = sparse.coo_matrix(items_features)

		self.model.fit_partial(user_ratings, user_features=users_features,
							item_features=items_features, epochs=epochs)

	def save_model(self):
		folder = 'model/'
		file_name = 'model.pickle'
		path = os.path.realpath(__file__)
		path = path.split('/')
		path.pop()
		path = '/'.join(path)
		full_file_name = os.path.join(path, folder, file_name)
		with open(full_file_name, 'wb') as file:
			pickle.dump(self.model, file, protocol=pickle.HIGHEST_PROTOCOL)

	def load_model(self):
		folder = 'model/'
		file_name = 'model.pickle'
		path = os.path.realpath(__file__)
		path = path.split('/')
		path.pop()
		path = '/'.join(path)
		full_file_name = os.path.join(path, folder, file_name)
		with open(full_file_name, 'rb') as file:
			self.model = pickle.load(file)

	def load_random_users(self):
		folder = 'model/'
		file_name = 'random.txt'
		path = os.path.realpath(__file__)
		path = path.split('/')
		path.pop()
		path = '/'.join(path)
		full_file_name = os.path.join(path, folder, file_name)
		with open(full_file_name, 'rb') as file:
			return pickle.load(file)

	def load_number_of_users(self):
		folder = 'model/'
		file_name = 'users_number.txt'
		path = os.path.realpath(__file__)
		path = path.split('/')
		path.pop()
		path = '/'.join(path)
		full_file_name = os.path.join(path, folder, file_name)
		with open(full_file_name, 'rb') as file:
			return pickle.load(file)

	def save_number_of_users(self, number):
		folder = 'model/'
		file_name = 'users_number.txt'
		path = os.path.realpath(__file__)
		path = path.split('/')
		path.pop()
		path = '/'.join(path)
		full_file_name = os.path.join(path, folder, file_name)
		with open(full_file_name, 'wb') as file:
			pickle.dump(number, file, protocol=pickle.HIGHEST_PROTOCOL)

	def train_new_user(self, user_features, items_features):
		self.train(user_features, items_features, epochs=5)

	def predict(self, user_features, items_features, restaurants_around, trained_user, restaurants_min_id, number_to_return = 5):
		number_of_restaurants = len(items_features)

		if (not trained_user):
			self.train_new_user(user_features, items_features)	
	

		items_features = sparse.coo_matrix(items_features)
		user_features = sparse.csr_matrix(user_features)


		scores = self.model.predict(0, item_ids=np.arange(number_of_restaurants), 
									user_features=user_features, item_features=items_features)

		
		return self.__select_restaurants_around(restaurants_around, np.argsort(-scores), number_to_return, restaurants_min_id), trained_user


	def __select_restaurants_around(self, restaurants_around, ml_restaurants, number_to_return, restaurants_min_id):
		ml_restaurants = [el + restaurants_min_id for el in ml_restaurants]
		to_return = [el for el in ml_restaurants if el in restaurants_around]
		return to_return[:number_to_return]