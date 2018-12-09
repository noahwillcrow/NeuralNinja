#Basic implementation of Mean Squared Error loss function

import numpy as np

class MeanSquaredError:
	def eval_error(self, input_vector, target_vector): #Evaluate the loss function
		squared_error_vector = np.square(target_vector - input_vector)
		return squared_error_vector.sum() / squared_error_vector.shape[0]

	def eval_error_grad(self, input_vector, target_vector): #Evaluate the derivative of the loss function
		return input_vector - target_vector
