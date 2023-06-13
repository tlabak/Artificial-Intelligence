import common

# Binary classifier prediction function
def predict1(x, y, weights, bias):
    activation = weights[0] * x + weights[1] * y + weights[2] * bias
    return 1 if activation >= 0 else 0

# Multi-class classifier prediction function
def predict2(x, y, weights):
    max_activation = float('-inf')
    predicted_class = -1

    # Iterate over each class and calculate the activation value
    for i in range(common.constants.NUM_CLASSES):
        activation = weights[i][0] * x + weights[i][1] * y
        # Track the class with the maximum activation value
        if activation > max_activation:
            max_activation = activation
            predicted_class = i

    return predicted_class

# Problem 1: Binary classifier
def part_one_classifier(data_train, data_test):
    # Initialize weights with bias feature
    weights = [0.0, 0.0, 0.0]
    bias = 1.0
    learning_rate = 0.1

    # TRAIN the perceptron
    for _ in range(common.constants.TRAINING_SIZE):
        for data in data_train:
            x, y, label = data
            # prediction using predict1 function
            prediction = predict1(x, y, weights, bias)
            # Calculate the error and update the weights
            error = label - prediction
            weights[0] += learning_rate * error * x
            weights[1] += learning_rate * error * y
            weights[2] += learning_rate * error * bias

    # TEST the perceptron on data_test
    for data in data_test:
        x, y, _ = data
        # prediction using predict1 function
        prediction = predict1(x, y, weights, bias)
        data[2] = prediction


# Problem 2: Multi-class classifier
def part_two_classifier(data_train, data_test):
    # Initialize weights for each class
    weights = [[0.0, 0.0] for _ in range(common.constants.NUM_CLASSES)]
    learning_rate = 0.1

    # TRAIN the perceptrons for each class
    for _ in range(common.constants.TRAINING_SIZE):
        for data in data_train:
            x, y, label = data
            # prediction using predict2 function
            prediction = predict2(x, y, weights)
            if label != prediction:
                # Update the weights based on the prediction and true label
                weights[int(label)][0] += learning_rate * x
                weights[int(label)][1] += learning_rate * y
                weights[int(prediction)][0] -= learning_rate * x
                weights[int(prediction)][1] -= learning_rate * y

    # TEST the perceptrons on data_test
    for data in data_test:
        x, y, _ = data
        # prediction using predict2 function
        prediction = predict2(x, y, weights)
        data[2] = prediction
