#Simple function for saving and loading a neural network
#The file structure is as follows
#2 bytes "magic" so we know the file type is correct
#2 bytes indicating how many layers are in the network
#A table with 2 4-byte entries for every layer in the network
#Each entry in the layer table gives the offset (in bytes) to the start and end of a layer
#Each layer has a variable format. They all start with a 1 byte "magic" value to indicate the layer type.
#This is then followed by a layer-type dependent header indicating metadata about the layer.
#The layer metadata is then followed by the actual parameters of the layer, if any.
#See the "from_serialized" and "serialize" methods in the layer files for more details

import struct

from layers.fullyConnected import FullyConnectedLayer
from layers.conv import Conv1DLayer
from layers.conv2D import TwoDConvolution
from layers.relu import ReluLayer
from layers.sigmoid import SigmoidLayer

def serialize_network(network, output_filename):
	file_body_array = []
	for layer in network:
		file_body_array.append(layer.serialize())

	header_string = struct.pack("<HH", 0x4E4E, len(file_body_array))
	offset = 4 + 8*len(file_body_array)
	layer_table_string = bytes()
	file_body_string = bytes()

	for serialized_layer in file_body_array:
		layer_table_string = layer_table_string + struct.pack("<II", offset, offset + len(serialized_layer))
		offset = offset + len(serialized_layer)
		file_body_string = file_body_string + serialized_layer

	output_file = open(output_filename, 'w+b')
	output_file.write(header_string + layer_table_string + file_body_string)
	output_file.close()

def deserialize_network(input_filename):
	input_file = open(input_filename, mode='rb')
	serialized_network = input_file.read()
	input_file.close()

	magic, num_layers = struct.unpack("<HH", serialized_network[:4])
	if magic != 0x4E4E:
		return None

	network = []
	layer_dict = {
		0xC1: lambda layer: Conv1DLayer.from_serialized(layer),
		0xFC: lambda layer: FullyConnectedLayer.from_serialized(layer),
		0x10: lambda layer: ReluLayer.from_serialized(layer),
		0xCC: lambda layer: TwoDConvolution.from_serialized(layer),
		0x55: lambda layer: SigmoidLayer.from_serialized(layer)
	}
	for i in range(0, num_layers):
		table_offset = i*8 + 4
		start, end = struct.unpack("<II", serialized_network[table_offset:table_offset+8])
		serialized_layer = serialized_network[start:end]
		network.append(layer_dict[int(serialized_layer[0])](serialized_layer))

	return network
