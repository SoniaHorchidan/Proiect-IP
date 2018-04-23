import numpy as np
from lightfm import LightFM
from scipy import sparse
import pickle
import os

class RestaurantRecommender:
	def __init__(self):
		self.model = LightFM(loss='warp')

	def train(self, users_features, items_features):
		# prepare data

		# eventually save the random generated users locally, load them
		# and add the new users (if any exists) as the last users
		number_of_users, number_of_features = users_features.shape
		number_of_restaurants = len(items_features)
		user_ratings = np.matrix(np.zeros((number_of_users, number_of_restaurants)))
		user_ratings = sparse.coo_matrix(user_ratings)
		users_features = sparse.coo_matrix(users_features)
		items_features = sparse.coo_matrix(items_features)

		self.model.fit_partial(user_ratings, user_features=users_features,
							item_features=items_features, epochs=40)

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
		self.train(user_features, items_features)
		users_number = self.load_number_of_users()
		self.save_number_of_users(users_number + 1)
		return users_number + 1
		

	def predict(self, user_features, items_features, restaurants_around, user_id = None, trained_user = False, number_to_return = 3):
		number_of_restaurants = len(items_features)
		# if (not trained_user):
		# 	user_number = self.train_new_user(user_features, items_features)
		# 	user_id = user_number
		# else:
		# 	user_number = -1
		items_features = sparse.coo_matrix(items_features)
		user_features = sparse.csr_matrix(user_features)

		# mock
		user_id = None
		if (user_id == None):
			user_ratings = np.zeros(number_of_restaurants)
			user_number = -1
		else:
			user_ratings = user_id # + number of random generated users for training


		scores = self.model.predict(user_ratings, item_ids=np.arange(number_of_restaurants), 
									user_features=user_features, item_features=items_features)

		return self.__select_restaurants_around(restaurants_around, np.argsort(-scores), number_to_return), user_number


	def __select_restaurants_around(self, restaurants_around, ml_restaurants, number_to_return):
		ml_restaurants = [el + 1 for el in ml_restaurants]
		to_return = [el for el in ml_restaurants if el in restaurants_around]
		return to_return[:number_to_return]




# some static mocked data

# mock_restaurants= {0: "La mama",
# 				  1: "Cel mai tare restaurant",
# 				  2: "Am mai fost aici",
# 				  3: "Caine",
# 				  4: "Fire",
# 				  5: "Gordon Ramsey's Restaurant",
# 				  6: "KFC",
# 				  7: "Spring Time"}

# restaurants_around = [0, 4, 6, 7]


# mock_features = ['sushi', 'mamaliga', 'ciorba', 'pizza', 'burger']
# 				#   0		1			2			3		4


# features_dalea_adevarate_boss = ['chicken', 'pork', 'pizza', 'burger', 'fish', 'sausage',
# 								 'beef', 'vegetarian', 'seafood', 'italian', 'sushi',
# 								 'mexican', 'asian', 'dessert', 'indian', 'soup', 'pasta',
# 								 'sandwich', 'shawarma', 'salad']


# mock_users_ratings = np.matrix([[0, 0, 0, 0, 0, 0, 0, 0],
# 							   [0, 0, 0, 0, 0, 0, 0, 0],
# 							   [0, 0, 0, 0, 0, 0, 0, 0],
# 							   [0, 0, 0, 0, 0, 0, 0, 0],
# 							   [0, 0, 0, 0, 0, 0, 0, 0]])

# mock_users_features = np.matrix([[0, 1, 1, 0, 0],
# 								[0, 0, 0, 1, 1],
# 								[1, 0, 0, 1, 1],
# 								[1, 0, 0, 0, 0],
# 								[0, 1, 1, 1, 1]])


# mock_items_features = np.matrix([[0, 1, 1, 0, 0],
# 								[0, 1, 1, 1, 1],
# 								[0, 1, 1, 0, 0],
# 								[1, 0, 0, 0, 0],
# 								[0, 0, 0, 1, 1],
# 								[0, 1, 1, 1, 1],
# 								[0, 0, 0, 0, 1],
# 								[0, 0, 0, 1, 1]])

# mock_single_user_features1 = np.matrix([[0, 1, 1, 0, 0]])
# mock_single_user_features2 = np.matrix([[1, 0, 0, 0, 0]])
# mock_single_user_features3 = np.matrix([[0, 0, 0, 1, 1]])
# mock_single_user_features4 = np.matrix([[0, 0, 1, 0, 1]])

# # mock_users_ratings = sparse.coo_matrix(mock_users_ratings)
# # mock_users_features = sparse.coo_matrix(mock_users_features)
# # mock_items_features = sparse.coo_matrix(mock_items_features)



# # some tests

# recommender = RestaurantRecommender()
# recommender.train(mock_users_features, mock_items_features)
# recommender.save_model()
# predicted_array = recommender.predict(mock_single_user_features1, mock_items_features,
# 									restaurants_around)
# print(predicted_array)

# predicted_array = recommender.predict(mock_single_user_features2, mock_items_features,
# 									restaurants_around)
# print(predicted_array)

# predicted_array = recommender.predict(mock_single_user_features3, mock_items_features,
# 									restaurants_around)
# print(predicted_array)

# predicted_array = recommender.predict(mock_single_user_features4, mock_items_features,
# 									restaurants_around)
# print(predicted_array)


