import unittest
import numpy as np
import numpy.testing
from layers.sigmoid import SigmoidLayer
import math

class TestSigmoidLayer(unittest.TestCase):
	def test_forward(self):
		layer = SigmoidLayer(3, 3)
		output = layer.forward(np.array([-1, 0, 1]))
		expected_output = np.array([1/(1+math.exp(1)), 0.5, 1/(1+math.exp(-1))])
		numpy.testing.assert_array_equal(output, expected_output)

	def test_backward(self):
		layer = SigmoidLayer(3, 3)
		output = layer.forward(np.array([-1, 0, 1]))
		expected_output = np.array([1/(1+math.exp(1)), 0.5, 1/(1+math.exp(-1))])
		expected_backwards = np.array([[expected_output[0]*(1-expected_output[0]), expected_output[1]*(1-expected_output[1]), expected_output[2]*(1-expected_output[2])]])
		backwards_output = layer.backward(np.array([1, 1, 1]))
		numpy.testing.assert_array_equal(backwards_output, expected_backwards)
