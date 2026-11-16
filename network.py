import numpy as np
import utils as u

class NeuralNetwork:
    # 'num_neurons' is an array of the number of neurons at each level.
    def __init__(self, num_neurons):
        # Stores each level
        self.levels = []

        # Iterate through every level
        for i in range (len(num_neurons) - 1):
            # Checks if its the output layer
            is_last = (i == len(num_neurons) - 2)

            # Make its level, where the no of inputs is at i
            # and the no of outputs is at i+1, then add level to array.
            level = Level(num_neurons[i], num_neurons[i + 1], output_layer=is_last)
            self.levels.append(level)

    # Takes input data, pushes it all the way through the network
    def feedForward(self, given_inputs):
        # Takes starting inputs and feeds through first level of the network
        # The result of this is the output.
        outputs = self.levels[0].feedForward(given_inputs)

        # Now loop through all remaining levels, start at index 1 as level 0 is above.
        for i in range (1, len(self.levels)):
            # Feed through current level, using previous layers outputs as inputs.
            outputs = self.levels[i].feedForward(outputs)

        # Return the final values, this is the values after its been fed through all layers.
        return outputs

    # This mutates it by amount (between 0 and 1)
    def mutate(self, amount):
        for l in self.levels:
            l.biases = u.lerp(l.biases, np.random.uniform(-1, 1, size=l.biases.shape), amount)
            l.weights = u.lerp(l.weights, np.random.uniform(-1, 1, size=l.weights.shape), amount)

class Level:
    def __init__(self, num_input, num_output, output_layer=False):
        # Each Level is a pair of input and output layer
        self.inputs = np.zeros(num_input)
        self.outputs = np.zeros(num_output)
        self.biases = np.zeros(num_output)
        self.output_layer = output_layer

        # Prepare weight array so each input maps to every output
        self.weights = np.zeros((num_input, num_output))

        self.randomise()

    # Randomises weights and biases to give a random brain   
    def randomise(self):
        self.weights = np.random.uniform(-1, 1, size = self.weights.shape)
        self.biases = np.random.uniform(-1, 1, size = self.biases.shape)

    # Feeds the given inputs forward by running through weights and comparing to bias (threshold).
    def feedForward(self, given_inputs):
        # Moves given inputs as the levels input
        for i in range (len(self.inputs)):
            self.inputs[i] = given_inputs[i]

        # For every output
        for i in range (len(self.outputs)):
            total = 0

            # Multiplies each input by its weight and add to sum - "Weighted vote"
            for j in range(len(self.inputs)):
                total += self.inputs[j] * self.weights[j][i]

            if self.output_layer:
                # If its the output layer, check if its greater than the threshold
                # This would mean its considered important enough to turn on.
                if (total > self.biases[i]):
                    # Turn it on
                    self.outputs[i] = 1
                # Otherwise, turn it off, or in this case, do not press
                else:
                    # Turn it off
                    self.outputs[i] = 0
            # If its hidden layer, apply tanh activation function
            else:
                self.outputs[i] = np.tanh(total - self.biases[i])

        return self.outputs
