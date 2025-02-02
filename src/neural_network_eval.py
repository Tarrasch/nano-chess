import pickle
from typing import List, Dict
import math

FILE_PATH = "models/first_attempt.pickle"

with open(FILE_PATH, "rb") as f:
    model_weights_dict: Dict[str, List[List[float]]] = pickle.load(f)

network_0_weights: List[List[float]] = model_weights_dict[
    "network.0.weight"
]  # List of length 16, each element is a list of 768 floats
network_0_weights_T: List[List[float]] = list(zip(*network_0_weights)) # List of length 768, each element is a list of 16 floats
network_2_weights: List[List[float]] = model_weights_dict[
    "network.2.weight"
]  # List of length 16, each element is a list of 16 floats
network_4_weights: List[List[float]] = model_weights_dict[
    "network.4.weight"
]  # List of length 16, each element is a list of 16 floats
network_6_weights: List[float] = model_weights_dict["network.6.weight"][
    0
]  # A list of 16 floats


def forward_pass_input_to_output_2(
    one_hot_encoded_board: List[int],
) -> float:
    # Layer 0
    layer_0_output = [
        sum(w * x for w, x in zip(weights, one_hot_encoded_board))
        for weights in network_0_weights
    ]
    layer_1_output = [math.tanh(x) for x in layer_0_output]

    return layer_1_output


def forward_pass_from_output2(
    layer_1_output: List[int],
) -> float:
    # Layer 2
    layer_2_output = [
        sum(w * x for w, x in zip(weights, layer_1_output))
        for weights in network_2_weights
    ]
    layer_3_output = [math.tanh(x) for x in layer_2_output]

    # Layer 4
    layer_4_output = [
        sum(w * x for w, x in zip(weights, layer_3_output))
        for weights in network_4_weights
    ]
    layer_5_output = [math.tanh(x) for x in layer_4_output]

    # Layer 6
    final_output = sum(w * x for w, x in zip(network_6_weights, layer_5_output))
    return final_output


def forward_pass(
    one_hot_encoded_board: List[int],
) -> float:
    return forward_pass_from_output2(
        forward_pass_input_to_output_2(one_hot_encoded_board)
    )
