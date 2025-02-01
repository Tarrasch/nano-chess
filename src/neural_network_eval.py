import pickle
from typing import List, Dict

FILE_PATH = "models/first_attempt.pickle"

with open(FILE_PATH, "rb") as f:
    model_weights_dict: Dict[str, List[List[float]]] = pickle.load(f)

network_0_weights: List[List[float]] = model_weights_dict[
    "network.0.weight"
]  # List of length 16, each element is a list of 768 floats
network_2_weights: List[List[float]] = model_weights_dict[
    "network.2.weight"
]  # List of length 16, each element is a list of 16 floats
network_4_weights: List[List[float]] = model_weights_dict[
    "network.4.weight"
]  # List of length 16, each element is a list of 16 floats
network_6_weights: List[float] = model_weights_dict[
    "network.6.weight"
][0]  # A list of 16 floats
