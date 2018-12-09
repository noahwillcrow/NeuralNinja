import numpy as np
import struct
from layers.baselayer import Layer

class Conv1DLayer(Layer):
	def __init__(self, input_dims, kernel_size):
		if input_dims < kernel_size:
			kernel_size = input_dims
		Layer.__init__(self, "conv1d", input_dims, input_dims - kernel_size + 1)
		self.kernel_size = kernel_size
		self.bias = np.random.rand(1) #Just as the weights are shared, so is the bias
		self.__create_kernel()
		self.create_weight_matrix_from_kernel()

	def forward(self, input_vector): #Same as the fully connected layer, except the weights and biases are connected together
		self.input_vector = input_vector
		self.output_vector = self.weight_matrix.dot(input_vector)
		self.output_vector += self.bias * np.ones((self.output_vector.shape[0]))
		return self.output_vector

	def backward(self, output_grad):
		bias_grad = np.sum(output_grad)
		weight_grad = (np.reshape(output_grad, (-1, 1))).dot(np.reshape(self.input_vector, (-1, 1)).transpose())
		kernel_grad = np.zeros(self.kernel.shape)
		for i in range(0, self.kernel_size): #Find the gradients of the weight matrix in the normal way, and then sum up along each mask to find the gradient with respect to the kernel
			kernel_grad[i] = np.sum(weight_grad * self.generate_mask(i))
	
		input_grad = self.weight_matrix.transpose().dot(output_grad)
		return [kernel_grad, bias_grad, input_grad]

	def update_from_grad(self, gradients, learning_rate):
		self.bias = self.bias - (gradients[1] * learning_rate)
		self.kernel = self.kernel - (gradients[0] * learning_rate)
		self.create_weight_matrix_from_kernel() #Only need to recompute the weight matrix after an update to the kernel

	def can_learn(self):
		return True

	def create_weight_matrix_from_kernel(self): #Creates a weight matrix from the current kernel parameters
		self.weight_matrix = np.zeros((self.output_dims, self.input_dims))
		for i in range(0, self.kernel_size):
			self.weight_matrix += self.generate_mask(i) * self.kernel[i]

	def generate_mask(self, offset): #Generates a mask representing what parts of the weight matrix correspond to which component of the kernel
		ret = np.zeros((self.output_dims, self.input_dims))
		for i in range(0, self.output_dims):
			ret[i, i+offset] = 1

		return ret

	def serialize(self):
		header_string = struct.pack("<BHH", 0xC1, self.input_dims, self.kernel_size)
		kernel_string = self.kernel.tobytes()
		bias_string = self.bias.tobytes()
		return header_string + kernel_string + bias_string

	@classmethod
	def from_serialized(cls, serialization_string):
		magic, input_dims, kernel_size = struct.unpack("<BHH", serialization_string[0:5])
		kernel = np.frombuffer(serialization_string[5:5+kernel_size*8])
		bias = np.frombuffer(serialization_string[5+kernel_size*8:])
		ret = cls(input_dims, kernel_size)
		ret.kernel = kernel
		ret.bias = bias
		return ret

	def __create_kernel(self):
		self.kernel = np.random.rand(self.kernel_size, 1) * 2 - 1

	def change_input_dims(self, new_input_dims):
		Layer.change_input_dims(self, new_input_dims)
		if new_input_dims < self.kernel_size:
			self.kernel_size = new_input_dims
			self.__create_kernel()
		Layer.change_output_dims(self, self.input_dims - self.kernel_size + 1)
		self.create_weight_matrix_from_kernel()

	def change_output_dims(self, new_output_dims):
		new_kernel_size = new_output_dims - self.input_dims - 1
		if new_kernel_size <= 0:
			self.kernel_size = 1
			self.change_input_dims(new_output_dims)
			return

		self.kernel_size = new_kernel_size
		self.__create_kernel()
		Layer.change_output_dims(self, self.input_dims - self.kernel_size + 1)
		self.create_weight_matrix_from_kernel()
