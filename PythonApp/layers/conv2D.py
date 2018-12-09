import numpy as np
from layers.baselayer import Layer
import struct

class TwoDConvolution(Layer):
	def __init__(self, input_dims, kernel_width, kernel_height, image_width, image_height):
		self.image_width = image_width
		self.image_height = image_height
		self.kernel = np.random.rand(kernel_height, kernel_width) * 2 - 1
		self.bias = np.random.rand(1)
		self.output_width = self.image_width - kernel_width + 1
		self.output_height = self.image_height - kernel_height + 1
		Layer.__init__(self, "conv2d", input_dims, self.output_width * self.output_height)
		self.create_weight_matrix_from_kernel()

	def forward(self, input_vector): #Similar to 1D convolution in that the equation is the same as fully connected, but weights and biases are tied together
		self.input_vector = input_vector
		self.output_vector = self.weight_matrix.dot(input_vector)
		self.output_vector += self.bias * np.ones((self.output_vector.shape[0]))
		return self.output_vector

	def backward(self, output_grad): #Again, similar to 1D convolution. Find the gradients with respect to the equivalent weight matrix. For each component of the kernel, sum over all of its respective elements in the weight gradient using the mask
		bias_grad = np.sum(output_grad)
		weight_grad = (np.reshape(output_grad, (-1, 1))).dot(np.reshape(self.input_vector, (-1, 1)).transpose())
		kernel_grad = np.zeros(self.kernel.shape)
		for i in range(0, self.kernel.shape[0]):
			for j in range(0, self.kernel.shape[1]):
				kernel_grad[i, j] = np.sum(self.generate_mask(i, j) * self.weight_matrix)

		input_grad = self.weight_matrix.transpose().dot(output_grad)
		return [kernel_grad, bias_grad, input_grad]

	def update_from_grad(self, gradients, learning_rate): 
		self.kernel = self.kernel - gradients[0]*learning_rate
		self.bias = self.bias - gradients[1]*learning_rate
		self.create_weight_matrix_from_kernel() #Only need to update the equivalent weight matrix when the kernel changes

	def can_learn(self):
		return True

	#Generates a binary mask that represents the location of an individual kernel parameter in the weight matrix
	#Same as the 1D equivalent, but more complicated because of how 2D convolution works
	#Think of a rectangular binary window with a single 1 sliding over a larger rectangle. Now unroll this setup row-wise. Repeat this process for each possible position of the window.
	def generate_mask(self, y, x):
		ret = np.zeros((self.output_dims, self.input_dims))
		kernel_height = self.kernel.shape[0]
		kernel_width = self.kernel.shape[1]
		for i in range(0, self.output_height):
			for j in range(0, self.output_width):
				ret[j + i*self.output_width, j+x + (i+y)*self.image_width] = 1

		return ret

	def create_weight_matrix_from_kernel(self): #Same as in 1D convolution, multiply the mask by the respective kernel value, add them all up, create an equivalent weight matrix
		self.weight_matrix = np.zeros((self.output_dims, self.input_dims))
		for i in range(0, self.kernel.shape[0]):
			for j in range(0, self.kernel.shape[1]):
				self.weight_matrix = self.weight_matrix + self.generate_mask(i, j) * self.kernel[i, j]

	def serialize(self):
		header_string = struct.pack("<BHHHHH", 0xCC, self.input_dims, self.kernel.shape[1], self.kernel.shape[0], self.image_width, self.image_height)
		kernel_string = self.kernel.tobytes()
		bias_string = self.bias.tobytes()
		return header_string + kernel_string + bias_string

	@classmethod
	def from_serialized(cls, serialization_string):
		magic, input_dims, kernel_width, kernel_height, image_width, image_height = struct.unpack("<BHHHHH", serialization_string[0:11])
		kernel = np.frombuffer(serialization_string[9:9+(kernel_width*kernel_height*8)]).reshape((kernel_height, kernel_width))
		bias = np.frombuffer(serialization_string[9+(kernel_width*kernel_height*8):])
		ret = cls(input_dims, kernel_width, kernel_height, image_width, image_height)
		ret.kernel = kernel
		ret.bias = bias
		return ret
