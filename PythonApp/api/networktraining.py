import argparse

import api.apicache as apicache
import api.apiregistry as apiregistry
from api.responsemodels.baseresponse import SuccessResponse

"""
Is used to train the network by using the input and target files and other arguments.
"""
def train_network(input_file_path, target_file_path, batch_size, num_epochs, learning_rate):
	apicache.current_network.train(input_file_path, target_file_path, batch_size, num_epochs, learning_rate)
	return SuccessResponse()

"""
Is used to evaluate the network
"""
def evaluate_network():
	if not apicache.current_network:
		raise Exception("No network established")
	error_rate = apicache.current_network.test_validation_accuracy()

	response = SuccessResponse()
	response.data["errorRate"] = error_rate
	return response

"""
Registers all APIs for this file
"""
def register_all_apis():
	train_network_arg_parser = argparse.ArgumentParser(description="Train network")
	train_network_arg_parser.add_argument("input_file_path", type=str)
	train_network_arg_parser.add_argument("target_file_path", type=str)
	train_network_arg_parser.add_argument("batch_size", type=int)
	train_network_arg_parser.add_argument("num_epochs", type=int)
	train_network_arg_parser.add_argument("learning_rate", type=float)
	apiregistry.register_action("train_network", train_network, train_network_arg_parser)

	evaluate_network_arg_parser = argparse.ArgumentParser(description="Evaluate network")
	apiregistry.register_action("evaluate_network", evaluate_network, evaluate_network_arg_parser)
