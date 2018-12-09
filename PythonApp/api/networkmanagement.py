import argparse
import numpy as np

import api.apicache as apicache
import api.apiregistry as apiregistry
from api.responsemodels.baseresponse import SuccessResponse, NetworkChangeSuccessResponse

from layers.fullyConnected import FullyConnectedLayer
from layers.conv import Conv1DLayer
from layers.conv2D import TwoDConvolution

from layers.relu import ReluLayer
from layers.sigmoid import SigmoidLayer

from models.network import Network

__ACTIVATION_LAYERS = {
	"relu": ReluLayer,
	"sigmoid": SigmoidLayer
}

"""
Creates a brand new network
"""
def create_new(num_inputs, num_outputs):
	apicache.current_network = Network(num_inputs, num_outputs)

	return NetworkChangeSuccessResponse()

"""
Gets a weight matrix at layer_index
"""
def get_weight_matrix(layer_index):
	if not apicache.current_network:
		raise Exception("No network established")

	response = SuccessResponse()
	response.data["weightMatrix"] = get_normed_weight_matrix(layer_index).tolist()
	return response

"""
Retrieves the current network data in whole
"""
def retrieve_current_network_data():
	if not apicache.current_network:
		raise Exception("No network established")

	response = NetworkChangeSuccessResponse()
	response.data["weightMatrices"] = [get_normed_weight_matrix(i).tolist() for i in range(1, apicache.current_network.get_num_layers())]
	return response

"""
Resizes a layer
"""
def resize_layer(layer_index, new_size):
	if not apicache.current_network:
		raise Exception("No network established")

	apicache.current_network.resize_layer(layer_index, new_size)

	return NetworkChangeSuccessResponse()

"""
Removes a layer. Cannot remove first or last layers.
"""
def remove_layer(layer_index):
	if not apicache.current_network:
		raise Exception("No network established")

	apicache.current_network.remove_layer(layer_index)

	return NetworkChangeSuccessResponse()

"""
Adds a standard fully connected layer
"""
def add_fully_connected_layer(insert_index, activation_type, num_nodes):
	if not apicache.current_network:
		raise Exception("No network established")

	layer = FullyConnectedLayer(apicache.current_network.get_input_dims_for_layer(insert_index - 1), num_nodes)
	activation_layer = __ACTIVATION_LAYERS[activation_type](num_nodes, num_nodes)
	apicache.current_network.insert_layer(insert_index, layer, activation_layer)

	return NetworkChangeSuccessResponse()

"""
Adds a 1D convolutional layer
"""
def add_conv_1d_layer(insert_index, activation_type, kernel_size):
	if not apicache.current_network:
		raise Exception("No network established")

	layer = Conv1DLayer(apicache.current_network.get_input_dims_for_layer(insert_index - 1), kernel_size)
	activation_layer = __ACTIVATION_LAYERS[activation_type](layer.output_dims, layer.output_dims)
	apicache.current_network.insert_layer(insert_index, layer, activation_layer)

	return NetworkChangeSuccessResponse()

"""
Adds a 2D convolutional layer
"""
def add_conv_2d_layer(insert_index, activation_type, kernel_width, kernel_height, output_width, output_height):
	if not apicache.current_network:
		raise Exception("No network established")

	layer = TwoDConvolution(apicache.current_network.get_input_dims_for_layer(insert_index - 1), kernel_width, kernel_height, output_width, output_height)
	activation_layer = __ACTIVATION_LAYERS[activation_type](layer.output_dims, layer.output_dims)
	apicache.current_network.insert_layer(insert_index, layer, activation_layer)

	return NetworkChangeSuccessResponse()

"""
Gets a normalized version of the weight matrix at layer layer_index
"""
def get_normed_weight_matrix(layer_index: int):
	raw_weight_matrix = apicache.current_network.get_weight_matrix(layer_index)
	min_val = np.amin(raw_weight_matrix)
	max_val = np.amax(raw_weight_matrix)
	if min_val == max_val:
		return np.zeros_like(raw_weight_matrix)
	normed_weight_matrix = (((raw_weight_matrix - min_val) / (max_val - min_val)) - 0.5) * 2
	return normed_weight_matrix

"""
Registers all APIs for this file
"""
def register_all_apis():
	create_new_arg_parser = argparse.ArgumentParser(description="Create a new network")
	create_new_arg_parser.add_argument("num_inputs", type=int)
	create_new_arg_parser.add_argument("num_outputs", type=int)
	apiregistry.register_action("create_new", create_new, create_new_arg_parser)

	apiregistry.register_action("retrieve_current_network_data", retrieve_current_network_data, None)

	get_weight_matrix_arg_parser = argparse.ArgumentParser(description="Get the weight matrix for a particular layer")
	get_weight_matrix_arg_parser.add_argument("layer_index", type=int)
	apiregistry.register_action("get_weight_matrix", get_weight_matrix, get_weight_matrix_arg_parser)

	resize_layer_arg_parser = argparse.ArgumentParser(description="Resize a layer's output dimensions")
	resize_layer_arg_parser.add_argument("layer_index", type=int)
	resize_layer_arg_parser.add_argument("new_size", type=int)
	apiregistry.register_action("resize_layer", resize_layer, resize_layer_arg_parser)

	remove_layer_arg_parser = argparse.ArgumentParser(description="Remove a layer from the current network")
	remove_layer_arg_parser.add_argument("layer_index", type=int)
	apiregistry.register_action("remove_layer", remove_layer, remove_layer_arg_parser)

	add_fully_connected_layer_arg_parser = argparse.ArgumentParser(description="Add a fully connected layer")
	add_fully_connected_layer_arg_parser.add_argument("insert_index", type=int)
	add_fully_connected_layer_arg_parser.add_argument("activation_type", type=str)
	add_fully_connected_layer_arg_parser.add_argument("num_nodes", type=int)
	apiregistry.register_action("add_fully_connected_layer", add_fully_connected_layer, add_fully_connected_layer_arg_parser)

	add_conv_1d_layer_arg_parser = argparse.ArgumentParser(description="Add a 1D convolutional layer")
	add_conv_1d_layer_arg_parser.add_argument("insert_index", type=int)
	add_conv_1d_layer_arg_parser.add_argument("activation_type", type=str)
	add_conv_1d_layer_arg_parser.add_argument("kernel_size", type=int)
	apiregistry.register_action("add_conv_1d_layer", add_conv_1d_layer, add_conv_1d_layer_arg_parser)

	add_conv_2d_layer_arg_parser = argparse.ArgumentParser(description="Add a 2D convolutional layer")
	add_conv_2d_layer_arg_parser.add_argument("insert_index", type=int)
	add_conv_2d_layer_arg_parser.add_argument("activation_type", type=str)
	add_conv_2d_layer_arg_parser.add_argument("kernel_width", type=int)
	add_conv_2d_layer_arg_parser.add_argument("kernel_height", type=int)
	add_conv_2d_layer_arg_parser.add_argument("output_width", type=int)
	add_conv_2d_layer_arg_parser.add_argument("output_height", type=int)
	apiregistry.register_action("add_conv_2d_layer", add_conv_2d_layer, add_conv_2d_layer_arg_parser)
