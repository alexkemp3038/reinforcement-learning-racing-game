import numpy as np

class NeuralNetwork:
    # 'num_neurons' is an array of the number of neurons at each level.
    def __init__(self, num_neurons):
        # Stores each level
        self.levels = []

        # Iterate through every level
        for i in range (len(num_neurons) - 1):
            # Make its level, where the no of inputs is at i
            # and the no of outputs is at i+1, then add level to array.
            level = Level(num_neurons[i], num_neurons[i + 1])
            self.levels.append(level)

    # Takes input data, pushes it all the way through the network
    def feedForward(given_inputs, network):
        # Takes starting inputs and feeds through first level of the network
        # The result of this is the output.
        outputs = Level.feedForward(given_inputs, network.levels[0])

        # Now loop through all remaining levels, start at index 1 as level 0 is above.
        for i in range (1, network.levels.len()):
            # Feed through current level, using previous layers outputs as inputs.
            outputs = Level.feedForward(outputs, network.levels[i])

        # Return the final values, this is the values after its been fed through all layers.
        return outputs

class Level:
    def __init__(self, num_input, num_output):
        # Each Level is a pair of input and output layer
        self.inputs = np.zeros(num_input)
        self.outputs = np.zeros(num_output)
        self.biases = np.zeros(num_output)

        # Prepare weight array so each input maps to every output
        self.weights = np.zeros((num_input, num_output))

    def randomise(self):
        self.weights = np.random.uniform(-1, 1, size = self.weights.shape)
        self.biases = np.random.uniform(-1, 1, size = self.biases.shape)

    def feedForward(given_inputs, level):
        for i in range (level.inputs.len()):
            level.inputs[i] = given_inputs[i]

        # For every output
        for i in range (level.outputs.len()):
            sum = 0

            # Loop through inputs
            for j in range(level.inputs.len()):
                # Add the product between the j input and the weight
                # between the j input and the i output
                sum += level.inputs[j]*level.weights[j][i]

                # Then check if its greater than the bias of this output neuron.
                if (sum > level.biases[i]):
                    # Turn it on
                    level.outputs[i] = 1
                else:
                    # Turn it off
                    level.outputs[i] = 0
