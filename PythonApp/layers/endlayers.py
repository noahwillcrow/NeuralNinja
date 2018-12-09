import numpy as np
from layers.baselayer import Layer

#Wrapper class for loading input data from a file
class InputLayer(Layer):
	def __init__(self, input_file_path):
		self.dataset = np.genfromtxt(input_file_path, delimiter=',')
		Layer.__init__(self, "input", self.dataset.shape[1], self.dataset.shape[1])

	def get_dataset_size(self):
		return self.dataset.shape[0]

	def forward(self, data_index): #Initializes the forward pass
		self.output_vector = self.dataset[data_index, :]
		return self.output_vector

	def backward(self, output_grad): #Does not need to backpropogate
		return [output_grad]


#Wrapper class for loading expected outputs from a file
class OutputLayer(Layer):
	def __init__(self, input_dims, error_function=None, target_file_path=None):
		Layer.__init__(self, "output", input_dims, input_dims)
		if not target_file_path is None:
			self.targets = np.genfromtxt(target_file_path, delimiter=',')
			if len(self.targets.shape) == 1:
				self.targets = np.reshape(self.targets, (-1, 1))
		else:
			self.targets = None
		self.error_function = error_function

	def forward(self, input_vector, target_index=-1): #Outputs the value of the loss for the current training example, or just outputs the neural network's output depending on if a target index is given
		self.input_vector = input_vector

		if target_index != -1:
			self.output_vector = self.error_function.eval_error(input_vector, self.targets[target_index, :])
		else:
			self.output_vector = input_vector

		return self.output_vector

	def backward(self, target_index): #Start backpropogation using the derivative of the loss
		return [self.error_function.eval_error_grad(self.input_vector, self.targets[target_index, :])]
