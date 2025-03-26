import pickle
import numpy as np
from numpy.typing import NDArray

FILE_PATH = "models/first_attempt.pickle"

with open(FILE_PATH, "rb") as f:
    model_weights_dict = pickle.load(f)

# Convert weights to numpy arrays
network_0_weights = np.array(model_weights_dict["network.0.weight"], dtype=np.float32)  # (16, 768)
network_2_weights = np.array(model_weights_dict["network.2.weight"], dtype=np.float32)  # (16, 16)
network_4_weights = np.array(model_weights_dict["network.4.weight"], dtype=np.float32)  # (16, 16)
network_6_weights = np.array(model_weights_dict["network.6.weight"][0], dtype=np.float32)  # (16,)

def forward_pass_input_to_output_0(one_hot_encoded_board: NDArray[np.float32]) -> NDArray[np.float32]:
    return network_0_weights @ one_hot_encoded_board

def forward_pass_from_output_0(layer_0_output: np.ndarray) -> float:
    layer_1_output = np.tanh(layer_0_output)
    layer_2_output = network_2_weights @ layer_1_output
    layer_3_output = np.tanh(layer_2_output)
    layer_4_output = network_4_weights @ layer_3_output
    layer_5_output = np.tanh(layer_4_output)
    return float(network_6_weights @ layer_5_output)

def forward_pass(one_hot_encoded_board: NDArray[np.float32]) -> float:
    return forward_pass_from_output_0(
        forward_pass_input_to_output_0(one_hot_encoded_board)
    )
