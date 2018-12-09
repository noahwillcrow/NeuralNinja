import unittest
import numpy as np
import numpy.testing
from layers.fullyConnected import FullyConnectedLayer

class TestFullyConnectedLayer(unittest.TestCase):
	def test_forward(self):
		layer = FullyConnectedLayer(3, 3)
		layer.weight_matrix = np.eye(3)
		layer.bias_vector = np.ones(3) * 0.5
		output = layer.forward(np.array([1, 1, 1]))
		numpy.testing.assert_array_equal(output, np.array([1.5, 1.5, 1.5]))

	def test_backward(self):
		layer = FullyConnectedLayer(3, 3)
		layer.weight_matrix = np.eye(3)
		layer.bias_vector = np.ones(3) * 0.5
		layer.forward(np.array([1, 1, 1]))
		backward_results = layer.backward(np.array([1, 1, 1]))
		numpy.testing.assert_array_equal(backward_results[2], np.array([1, 1, 1]))
		numpy.testing.assert_array_equal(backward_results[1], np.array([1, 1, 1]))
		numpy.testing.assert_array_equal(backward_results[0], np.array([[1, 1, 1],
										[1, 1, 1],
										[1, 1, 1]]))

	def test_update_from_grad(self):
		layer = FullyConnectedLayer(3, 3)
		layer.weight_matrix = np.eye(3)
		layer.bias_vector = np.ones(3) * 0.5
		weight_grad = np.array([[1, 1, 1],
					[1, 1, 1],
					[1, 1, 1]])
		bias_grad = np.array([1, 1, 1])
		layer.update_from_grad([weight_grad, bias_grad], 0.5)
		numpy.testing.assert_array_equal(layer.weight_matrix, np.array([[0.5, -0.5, -0.5],
										[-0.5, 0.5, -0.5],
										[-0.5, -0.5, 0.5]]))
		numpy.testing.assert_array_equal(layer.bias_vector, np.array([0, 0, 0]))

