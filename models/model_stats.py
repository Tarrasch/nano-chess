import pickle
import numpy as np

print("hi")

FILE_PATH = "models/first_attempt.pickle"

with open(FILE_PATH, "rb") as f:
    model_weights_dict = pickle.load(f)

network_0_weights = model_weights_dict["network.0.weight"]

# Convert to numpy array for easier statistical analysis
network_0_weights_np = np.array(network_0_weights)

# Calculate statistics
mean = np.mean(network_0_weights_np)
std_dev = np.std(network_0_weights_np)
min_val = np.min(network_0_weights_np)
max_val = np.max(network_0_weights_np)

print(f"Shape of network.0.weight: {network_0_weights_np.shape}")
print(f"Mean of network.0.weight: {mean}")
print(f"Standard Deviation of network.0.weight: {std_dev}")
print(f"Minimum value in network.0.weight: {min_val}")
print(f"Maximum value in network.0.weight: {max_val}")
print(f"Num positives in network.0.weight: {sum(network_0_weights_np.flatten() > 0)}")
print(f"Num negatives in network.0.weight: {sum(network_0_weights_np.flatten() < 0)}")


# Check symmetry
symmetric_count = 0
total_count = 0
for i in range(768 // 2):
    rank = (i // 8) % 8  # 0-7 (1-8)
    file = i % 8  # 0-7 (a-h)
    square_black = (7 - rank) * 8 + file
    black_i = 768 // 2 + 64 * (i // 64) + square_black
    for j in range(16):
        total_count += 1
        if np.isclose(network_0_weights_np[j][i], -network_0_weights_np[j][black_i]):
            symmetric_count += 1

print(f"Number of symmetric entries: {symmetric_count} out of {total_count}")