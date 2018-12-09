#Defines a simple fully connected layer with no activation function

import numpy as np
from layers.baselayer import Layer
import struct

class FullyConnectedLayer(Layer):
	def __init__(self, input_dims, output_dims):
		Layer.__init__(self, "fullyConnected", input_dims, output_dims)
		self.__init_weight_matrix()
		self.bias_vector = np.random.rand(output_dims)*2-1

	def forward(self, input_vector): #y = wx + b
		self.input_vector = input_vector
		self.output_vector = self.weight_matrix.dot(input_vector) + self.bias_vector
		return self.output_vector

	def backward(self, output_grad):
		bias_grad = output_grad #dL/db = dL/dy
		weight_grad = (np.reshape(output_grad, (-1, 1))).dot(np.reshape(self.input_vector, (-1, 1)).transpose()) #dL/dW = dL/dy x^T
		input_grad = self.weight_matrix.transpose().dot(bias_grad) #dL/dx = W^T dL/dy
		return [weight_grad, bias_grad, input_grad]

	def update_from_grad(self, gradients, learning_rate):
		self.weight_matrix = self.weight_matrix - (gradients[0] * learning_rate) #w = w + eta * dL/dW
		self.bias_vector = self.bias_vector - (gradients[1] * learning_rate) #b = b + eta * dL/db

	def can_learn(self):
		return True

	def serialize(self):
		header_string = struct.pack("<BHH", 0xFC, self.input_dims, self.output_dims)
		weight_string = self.weight_matrix.tobytes()
		bias_string = self.bias_vector.tobytes()
		return header_string + weight_string + bias_string

	def change_input_dims(self, new_input_dims):
		Layer.change_input_dims(self, new_input_dims)
		self.__init_weight_matrix()

	def change_output_dims(self, new_output_dims):
		Layer.change_output_dims(self, new_output_dims)
		self.bias_vector = np.random.rand(self.output_dims)*2-1
		self.__init_weight_matrix()

	def __init_weight_matrix(self):
		self.weight_matrix = np.random.rand(self.output_dims, self.input_dims)*2-1

	@classmethod
	def from_serialized(cls, serialization_string):
		magic, input_dims, output_dims = struct.unpack("<BHH", serialization_string[0:5])
		weight_matrix = np.frombuffer(serialization_string[5:5+(input_dims*output_dims*8)]).reshape((output_dims, input_dims))
		bias_vector = np.frombuffer(serialization_string[5+(input_dims*output_dims*8):])
		ret = cls(input_dims, output_dims)
		ret.weight_matrix = weight_matrix
		ret.bias_vector = bias_vector
		return ret
