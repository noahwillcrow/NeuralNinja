#Simple implementation of batched Stochastic Gradient Descent to train an arbitrary neural network

import random
import numpy as np
from layers.endlayers import InputLayer, OutputLayer
from errorfunctions.mse import MeanSquaredError

class Trainer:
	def __init__(self, network, input_file_path, target_file_path):
		input_layer = InputLayer(input_file_path)
		output_layer = OutputLayer(network[-1].get_dims()[0], MeanSquaredError(), target_file_path)
		self.network = network.copy()
		self.network.insert(0, input_layer)
		self.network.append(output_layer)

	def process_example(self, example): #Compute the gradients for an individual training example
		gradients = [[]]
		output_vector = example
		gradient_vector = [example]

		#Forward pass
		for layer in self.network:
			output_vector = layer.forward(output_vector)

		#Backward pass
		for layer_index in range(len(self.network) - 1, -1, -1):
			while layer_index >= len(gradients):
				gradients.append([])

			gradient_vector = self.network[layer_index].backward(gradient_vector[-1])
			for parameter_index in range(0, len(gradient_vector)-1):
				if len(gradients[layer_index]) <= parameter_index:
					gradients[layer_index].append(gradient_vector[parameter_index])
				else:
					gradients[layer_index][parameter_index] += gradient_vector[parameter_index]

		return gradients

	def train(self, batch_size, num_epochs, learning_rate, training_indices=None):
		if training_indices is None:
			training_indices = list(range(0, self.network[0].get_dataset_size()))

		for _ in range(0, num_epochs): #Repeat entire procedure for desired number of epochs
			random.shuffle(training_indices) #Shuffle the training set

			batch_index = 0
			while batch_index < len(training_indices): #Break the current epoch into batches
				batch = training_indices[batch_index:min(batch_index + batch_size, len(training_indices))] #Get next batch

				results = []
				for example in batch:
					results.append(self.process_example(example)) #Compute the gradients for every example in our batch


				#Sum over all of the gradients in the batch
				gradients = results[0]
				for i in range(0, len(gradients)):
					for j in range(0, len(gradients[i])):
						gradients[i][j] = np.nan_to_num(gradients[i][j])

				for i in range(1, len(results)):
					current_gradient = results[i]
					for j in range(0, len(current_gradient)):
						for k in range(0, len(current_gradient[j])):
							gradients[j][k] += np.nan_to_num(current_gradient[j][k])
					

				#Update our parameters (flush gradients)
				for layer_index in range(0, len(self.network)):
					layer = self.network[layer_index]

					if layer.can_learn():
						layer.update_from_grad(gradients[layer_index], learning_rate)

				batch_index += batch_size


	#Simple test function that outputs the average of the loss function over the testing set
	#Note that we don't use accuracy metrics because we aren't necessarily trying to do classification, this library is designed to be highly modular
	def test(self, test_indices=None):
		if test_indices is None:
			test_indices = list(range(0, self.network[0].get_dataset_size()))

		error = 0.0
		for test_index in test_indices:
			output_vector = test_index

			for layer_index in range(0, len(self.network)-1):
				output_vector = self.network[layer_index].forward(output_vector)

			current_error = self.network[-1].forward(output_vector, test_index)
			error += current_error

		return error / len(test_indices)
