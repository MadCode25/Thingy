import numpy as np

# ===== ACTIVATION =====
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)


# ===== VISUALIZER =====
def draw_network(inputs, hidden, outputs, result):
    print("\n=== NEURAL NETWORK ===\n")

    max_len = max(len(inputs), len(hidden), len(outputs))

    for i in range(max_len):
        inp = f"{inputs[i]:.2f}" if i < len(inputs) else "   "
        hid = f"{hidden[i]:.2f}" if i < len(hidden) else "   "
        out = f"{outputs[i]:.2f}" if i < len(outputs) else "   "

        print(f"[{inp}] ---> ({hid}) ---> <{out}>")

    print("\\")
    print(f"\\---> ({result})")
    print("\n======================\n")


# ===== STORAGE =====
categories = []
category_map = {}

X_list = []
y_list = []

trained = False
epochs = 10000
considered_less = 0.8


# ===== COMMAND LOOP =====
while True:
    cmd = input(">> ").strip()

    # ===== DEFINE CATEGORIES =====
    if cmd.startswith("categorize"):
        categories = cmd.replace("categorize", "").strip().split()
        print("Categories:", categories)

    # ===== ASSIGN OUTPUTS =====
    elif cmd.startswith("arrange"):
        parts = cmd.split()
        name = parts[1]
        values = list(map(int, parts[2:]))

        category_map[name] = values
        print(f"{name} → {values}")

    # ===== ADD TRAINING DATA =====
    elif cmd.startswith("train"):
        try:
            left, right = cmd.replace("train", "").split("=")

            # INPUT
            x_vals = list(map(float, left.strip().replace(" ", "").split(",")))

            # OUTPUT (category OR raw vector)
            right = right.strip()

            if right in category_map:
                y_vals = category_map[right]
            else:
                y_vals = list(map(float, right.replace(" ", "").split(",")))

            # Validate output size consistency
            if len(y_list) > 0 and len(y_vals) != len(y_list[0]):
                print("Output size mismatch!")
                continue

            X_list.append(x_vals)
            y_list.append(y_vals)

            print("Added training sample.")

        except ValueError:
            print("Invalid format.")

    # ===== TRAIN MODEL =====
    elif cmd == "fit":
        if len(X_list) == 0:
            print("No training data!")
            continue

        X = np.array(X_list)
        y = np.array(y_list)

        np.random.seed(1)

        input_neurons = X.shape[1]
        hidden_neurons = 6
        output_neurons = len(y[0])

        W1 = np.random.uniform(size=(input_neurons, hidden_neurons))
        W2 = np.random.uniform(size=(hidden_neurons, output_neurons))

        for _ in range(epochs):
            hidden = sigmoid(np.dot(X, W1))
            output = sigmoid(np.dot(hidden, W2))

            error = y - output

            d_output = error * sigmoid_derivative(output)
            d_hidden = d_output.dot(W2.T) * sigmoid_derivative(hidden)

            W2 += hidden.T.dot(d_output) * 0.1
            W1 += X.T.dot(d_hidden) * 0.1

        trained = True
        print("Training complete!")

    # ===== PREDICT =====
    elif cmd.startswith("predict"):
        if not trained:
            print("Train first using 'fit'")
            continue

        try:
            raw = cmd[len("predict"):].strip()
            raw = raw.replace(",", " ")
            vals = list(map(float, raw.split()))

            if len(vals) != input_neurons:
                print(f"Expected {input_neurons} inputs, got {len(vals)}")
                continue

            test = np.array([vals])

            hidden = sigmoid(np.dot(test, W1))
            output = sigmoid(np.dot(hidden, W2))

            result = (output > considered_less).astype(int).flatten()

            # Match to category
            found = None
            for name, vec in category_map.items():
                if vec == result.tolist():
                    found = name
                    break

            print("Raw:", output.flatten())
            print("Vector:", result)

            if found:
                print("Prediction:", found)
                draw_network(test[0], hidden[0], output[0], found)
            else:
                print("Prediction: Unknown")

        except ValueError:
            print("Invalid input.")
    
    # ===== MODE =====
    elif cmd.startswith("mode"):
        parts = cmd.split()
        if parts[1] == "fast":
            epoch = 10000
        elif parts[1] == "too_smart":
            epoch = 1000000
        elif parts[1] == "slow":
            epoch = 1000
        elif parts[1] == "dumb":
            epoch = 300
        elif parts[1] == "toddler":
            epoch = 10
        elif parts[1] == "absolute_dumb":
            epoch = 0
        else:
            print("Unknown mode")
        print("Set mode to " + parts[1] + ", epoch", epoch)
        
    
    # ===== EXIT =====
    elif cmd == "exit":
        break

    else:
        print("Unknown command.")
