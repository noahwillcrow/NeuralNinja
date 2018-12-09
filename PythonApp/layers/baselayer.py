#Base class from which all layers inherit

import numpy as np

class Layer:
	def __init__(self, layer_type, input_dims, output_dims):
		self.__layer_type = layer_type
		self.input_dims = input_dims
		self.output_dims = output_dims
		self.input_vector = np.zeros((input_dims, 1))
		self.output_vector = np.zeros((output_dims, 1))

	def change_input_dims(self, new_input_dims):
		self.input_dims = new_input_dims
		self.input_vector = np.zeros((new_input_dims, 1))

	def change_output_dims(self, new_output_dims):
		self.output_dims = new_output_dims
		self.output_vector = np.zeros((new_output_dims, 1))

	def get_dims(self):
		return (self.input_dims, self.output_dims)

	def can_learn(self):
		return False

	def to_json(self):
		return {
			"layerType": self.__layer_type,
			"numNodes": self.output_dims
		}
