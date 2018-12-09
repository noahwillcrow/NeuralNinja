import argparse

import api.apicache as apicache
import api.apiregistry as apiregistry
from api.responsemodels.baseresponse import SuccessResponse, NetworkChangeSuccessResponse
from models.network import Network

"""
Saves the current network to a file
"""
def save_to_file(file_path):
	if not apicache.current_network:
		raise Exception("No network established")
	apicache.current_network.save_to_file(file_path)
	return SuccessResponse()

"""
Loads a file in as the current network
"""
def load_from_file(file_path):
	apicache.current_network = Network.load_from_file(file_path)
	return NetworkChangeSuccessResponse()

"""
Registers all APIs for this file
"""
def register_all_apis():
	save_to_file_arg_parser = argparse.ArgumentParser(description="Save network to file")
	save_to_file_arg_parser.add_argument("file_path", type=str)
	apiregistry.register_action("save_to_file", save_to_file, save_to_file_arg_parser)

	load_from_file_arg_parser = argparse.ArgumentParser(description="Load network from file")
	load_from_file_arg_parser.add_argument("file_path", type=str)
	apiregistry.register_action("load_from_file", load_from_file, load_from_file_arg_parser)
