#Logistic sigmoid activation function

import numpy as np
from layers.baselayer import Layer
import struct

class SigmoidLayer(Layer):
	def __init__(self, input_dims, output_dims):
		Layer.__init__(self, "sigmoid", input_dims, output_dims)
		
	def forward(self, input_vector): #1/(1 + e^(-x))
		self.input_vector = input_vector
		self.output_vector = 1 / (1 + np.exp(-input_vector))
		return self.output_vector

	def backward(self, output_grad): #dL/dx = dL/dy * y * (1 - y)
		return [self.output_vector * (1 - self.output_vector) * output_grad]

	def serialize(self):
		header_string = struct.pack("<BHH", 0x55, self.input_dims, self.output_dims)
		return header_string

	@classmethod
	def from_serialized(cls, serialization_string):
		magic, input_dims, output_dims = struct.unpack("<BHH", serialization_string)
		return cls(input_dims, output_dims)
