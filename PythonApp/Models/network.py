from layers.baselayer import Layer
from layers.fullyConnected import FullyConnectedLayer
from layers.sigmoid import SigmoidLayer
from networkserialization import serialize_network, deserialize_network
from trainer import Trainer

"""
The key class for the APIs
"""
class Network:
    def __init__(self, input_dims: int, output_dims: int):
        self.__input_dims: int = input_dims
        self.__layers: list = [FullyConnectedLayer(input_dims, output_dims), SigmoidLayer(output_dims, output_dims)] # Initialize with output layer
        self.__trainer: Trainer = None

    """
    Gets the total number of layers. Does not count activation layers.
    """
    def get_num_layers(self):
        return len(self.__layers)//2 + 1 #/2 for activation layers, add one for input layer

    """
    Gets the input dimensions for a given layer
    """
    def get_input_dims_for_layer(self, layer_index: int):
        if layer_index == 0 or layer_index == 1:
            return self.__input_dims
        layers_array_index = self.__convert_to_array_index(layer_index)
        return self.__layers[layers_array_index].input_dims

    """
    Gets the output dimensions for a given layer
    """
    def get_output_dims_for_layer(self, layer_index: int):
        if layer_index == 0: # Output dims for input layer
            return self.__input_dims
        layers_array_index = self.__convert_to_array_index(layer_index)
        return self.__layers[layers_array_index + 1].output_dims # +1 for the activation layer

    """
    Gets the weight matrix for a given layer
    """
    def get_weight_matrix(self, layer_index: int):
        if layer_index == 0: # The input layer doesn't have a weight matrix
            raise Exception("Input layer does not have a weight matrix")
        layers_array_index = self.__convert_to_array_index(layer_index)
        return self.__layers[layers_array_index].weight_matrix

    """
    Inserts a new layer into this network using the given arguments
    """
    def insert_layer(self, insert_index: int, layer: Layer, activation_layer: Layer):
        if insert_index >= self.get_num_layers():
            raise Exception("Cannot add a hidden layer after the output layer")
        true_insert_index = self.__convert_to_array_index(insert_index)
        self.__layers.insert(true_insert_index, layer)
        self.__layers.insert(true_insert_index + 1, activation_layer)
        self.__layers[true_insert_index + 2].change_input_dims(activation_layer.output_dims)

    """
    Resizes a given layer if possible (may be recursive)
    """
    def resize_layer(self, layer_index: int, new_size: int):
        layers_array_index = -2

        if layer_index == 0: # Changing input layer size
            self.__input_dims = new_size
        else:
            layers_array_index = self.__convert_to_array_index(layer_index)
            old_input_dims = self.__layers[layers_array_index].input_dims

            self.__layers[layers_array_index].change_output_dims(new_size)
            new_output_dims = self.__layers[layers_array_index].output_dims # Some layers don't behave nicely

            self.__layers[layers_array_index + 1].change_input_dims(new_output_dims) # Update activation layer dims
            self.__layers[layers_array_index + 1].change_output_dims(new_output_dims)

            if self.__layers[layers_array_index].input_dims != old_input_dims:
                self.resize_layer(layer_index - 1, self.__layers[layers_array_index].input_dims)
        
        if layer_index < self.get_num_layers() - 1: # Changing any layer other than the output layer
            old_output_dims = self.__layers[layers_array_index + 2].output_dims
            self.__layers[layers_array_index + 2].change_input_dims(new_size)
            if self.__layers[layers_array_index + 2].output_dims != old_output_dims:
                self.resize_layer(layer_index + 1, self.__layers[0].output_dims)

    """
    Removes a layer
    """
    def remove_layer(self, layer_index: int):
        if layer_index == 0:
            raise Exception("Cannot delete input layer")
        if layer_index == self.get_num_layers() - 1:
            raise Exception("Cannot delete output layer")
        layers_array_index = self.__convert_to_array_index(layer_index)
        del self.__layers[layers_array_index] # Actual layer
        del self.__layers[layers_array_index] # Activation layer
        self.__layers[layers_array_index].change_input_dims(self.get_output_dims_for_layer(layer_index - 1))

    """
    Creates a trainer and runs on the network's layers
    """
    def train(self, input_file_path, target_file_path, batch_size, num_epochs, learning_rate, training_indices=None):
        self.__trainer = Trainer(self.__layers, input_file_path, target_file_path)
        self.__trainer.train(batch_size, num_epochs, learning_rate, training_indices)

    """
    Tests validation accuracy
    """
    def test_validation_accuracy(self, validation_indices=None):
        if not self.__trainer:
            raise Exception("Network not yet trained")
        return self.__trainer.test(validation_indices)

    """
    Saves the network to a file
    """
    def save_to_file(self, file_path):
        serialize_network(self.__layers, file_path)

    """
    Loads a Network from a file
    """
    @classmethod
    def load_from_file(cls, file_path):
        hidden_layers = deserialize_network(file_path)
        network = cls(hidden_layers[0].input_dims, hidden_layers[-1].output_dims)
        cls._set_hidden_layers(network, hidden_layers)
        return network

    """
    Used for the API
    """
    def to_json(self):
        actual_layers = [self.__layers[i * 2] for i in range(len(self.__layers)//2)]
        actual_layers.insert(0, Layer("input", self.__input_dims, self.__input_dims))

        return {
            "layers": [layer.to_json() for layer in actual_layers]
        }

    def _set_hidden_layers(self, hidden_layers: list):
        self.__layers = hidden_layers

    def __convert_to_array_index(self, outside_layer_index: int) -> int:
        # "outside layer" refers to the layers that the outside thinks exists.
        # The "outside" is unaware that each layer is really two - the layer itself and its activation layer
        if outside_layer_index < 0 or outside_layer_index >= self.get_num_layers():
            raise Exception("Layer index is out of bounds")
        if outside_layer_index == 0:
            return 0
        return 2 * (outside_layer_index - 1)
