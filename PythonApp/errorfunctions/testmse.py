import unittest
import numpy as np
import numpy.testing
from errorfunctions.mse import MeanSquaredError

class TestMeanSquaredError(unittest.TestCase):
	def test_eval_error(self):
		error_func = MeanSquaredError()
		output = error_func.eval_error(np.array([1, 2, 3, 0]), np.array([3, 2, 1, 0]))
		self.assertEqual(output, 2)

	def test_eval_error_grad(self):
		error_func = MeanSquaredError()
		output = error_func.eval_error_grad(np.array([1, 2, 3]), np.array([3, 2, 1]))
		numpy.testing.assert_array_equal(output, np.array([-2, 0, 2]))
