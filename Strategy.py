
import numpy as np

import random
import math

import keras
from keras.layers.merge import Multiply, Add, Concatenate
from keras.layers import Input, Dense, Dropout
from keras.models import Model


class Strategy:


	def __init__(self):

		self.model = self.getRandomModel()

		self.mem = 0.

		return

	def getAction(self, neighbor_colours, position):

		new_x = []
		for colour in neighbor_colours:
			h, s, v = colour

			# originally in [0, 1] so move to [-0.5, 0.5]
			h -= 0.5
			s -= 0.5
			v -= 0.5

			new_x.extend([h, s, v])

		new_x.append(self.mem) #np.random.uniform(-1, 1))
		new_x.extend(position)

		X = []
		X.append(new_x)

		X = np.array(X)

		action = self.model.predict(X)[0]

		dx = action[0]
		dy = action[1]

		dh = action[2]
		ds = action[3]
		dv = action[4]

		self.mem = action[5]

		dx = -1 if dx < 0.5 else (1 if dx > 0.5 else 0)
		dy = -1 if dy < 0.5 else (1 if dy > 0.5 else 0)
		
		return (dx, dy), (dh, ds, dv)

		#return (1, 1), (0, 0, 0)



	def getModifiedWeights(self, n, include_self=False):

		if include_self: n = n-1

		variations = []

		variations.append(self.model.get_weights())

		for _ in range(n):
			variations.append(self.modifyWeights(self.model.get_weights()))

		return variations


	def getRandomModel(self):

		input_layer = Input(shape=(30,)) # see getAction() what what each is
		dense_1 = Dense(32, activation='tanh')(input_layer)
		dense_1 = Dense(32, activation='tanh')(dense_1)
		#dense_1 = Dense(10, activation='tanh')(dense_1)
		output_1 = Dense(6, activation='tanh')(dense_1)

		model = Model(inputs=input_layer, outputs=output_1)

		# can get weights with model.get_weights()
		# can set weights with model.set_weights()

		return model

	def setWeights(self, new_weights):

		self.model.set_weights(new_weights)
		self.mem = 0.


def reproduceStrategies(parent_A, parent_B, mutation_rate=0.1):
	# parent_A and B should be of type Strategy

	def mutateStrategy(strategy):

		weights = strategy.model.get_weights()

		new_weights = []
		nb_matrices = len(weights)
		for i, w in enumerate(weights):
			r_l = 1.*i/(nb_matrices-1)

			mutation_level = np.random.uniform(0, mutation_rate)


			#w_new = w + np.random.normal(loc=0, scale=mutation_level, size=w.shape)
			rand_add_mask = np.random.choice([0., 1.], p=[0.9, 0.1], size=w.shape)
			w_new = w + np.random.normal(loc=0, scale=mutation_level, size=w.shape)*rand_add_mask

			#rand_mult_mask = np.random.choice([0., 1.], p=[0.01, 0.99], size=w.shape)
			#w_new = w_new*rand_mult_mask

			new_weights.append(w_new)

		return new_weights

	

	W1 = mutateStrategy(parent_A)

	W2 = mutateStrategy(parent_B)

	# finally combine W1 and W2
	new_weights = []
	bias = random.random()
	# TODO: make combining similar to humans -- take half 
	for w1, w2 in zip(W1, W2):

		mask = np.random.choice([0., 1.], p=[bias, 1-bias], size=w1.shape)

		w_new = w1*mask + w2*(1-mask)

		new_weights.append(w_new)

	return new_weights
