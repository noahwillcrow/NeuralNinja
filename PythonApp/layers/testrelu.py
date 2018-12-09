import unittest
import numpy as np
import numpy.testing
from layers.relu import ReluLayer

class TestReluLayer(unittest.TestCase):
	def test_forward(self):
		layer = ReluLayer(3, 3)
		output = layer.forward(np.array([-2, 1, 2]))
		numpy.testing.assert_array_equal(output, np.array([0, 1, 2]))

	def test_backward(self):
		layer = ReluLayer(3, 3)
		output = layer.forward(np.array([-2, 1, 2]))
		backward_results = layer.backward(np.array([1, 1, 1]))
		numpy.testing.assert_array_equal(backward_results[0], np.array([0, 1, 1]))
