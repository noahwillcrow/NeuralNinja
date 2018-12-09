#Rectified Linear Unit activation function

from layers.baselayer import Layer
import struct

class ReluLayer(Layer):
	def __init__(self, input_dims, output_dims):
		Layer.__init__(self, "ReLU", input_dims, output_dims)

	def forward(self, input_vector): #0 if x < 0, x if x >= 0
		self.input_vector = input_vector
		self.output_vector = input_vector.copy()
		self.output_vector[self.output_vector < 0] = 0
		return self.output_vector

	def backward(self, output_grad): #0 if x < 0, dL/dy if x >= 0
		ret = output_grad.copy()
		ret[self.input_vector < 0] = 0
		return [ret]

	def serialize(self):
		header_string = struct.pack("<BHH", 0x10, self.input_dims, self.output_dims)
		return header_string

	@classmethod
	def from_serialized(cls, serialization_string):
		magic, input_dims, output_dims = struct.unpack("<BHH", serialization_string)
		return cls(input_dims, output_dims)
