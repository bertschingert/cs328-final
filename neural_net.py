import numpy as np
import math

def logistic(x):
    return 1/(1+np.exp(-x))

def d_logistic(x):
    return x*(1-x)

def propagate(inp, w, b, f):
    return f(np.dot(w, inp) + b[:, None])

def error(target, computed):
    return 0.5 * (target - computed) ** 2

def derror(target, computed):
    return target - computed

def initialize_network(inp_length, outp_length, num_layers, num_hidden):
    global layers 
    layers = num_layers
    global weights
    global bias
    global input_length
    input_length = inp_length
    global output_length
    output_length = outp_length
    weights = []
    bias = []
    weights.append(np.random.rand(num_hidden, input_length))
    bias.append(np.random.rand(num_hidden))
    if layers > 2:
        for i in range(layers-2):
            weights.append(np.random.rand(num_hidden, num_hidden))
            bias.append(np.random.rand(num_hidden))
    weights.append(np.random.rand(output_length, num_hidden))
    bias.append(np.random.rand(outp_length))
    return weights
    
def set_hidden_units(layer, new_hidden):
    if layer == layers:
        print("No hidden units at this layer")
    else:
        weights[layer-1] = np.random.rand(new_hidden, weights[layer-1].shape[1])
        weights[layer] = np.random.rand(weights[layer].shape[1], new_hidden)
    return weights

def update_weights(input, output, eta):
    activations = []
    new_weights = []
    new_biases = []
    # not sure exactly how the looping while work, but will come back to this
    # and figure it out
    for i in range(input.shape[1]):
        activation = []
        weight = []
        bias = []
        x0 = input[:, [i]]
        for j in range(layers):
            if i == 0:
                activation.append(propagate(x0, weights[0], bias[0], logistic))
            else:
                activation.append(propagate(activation[j-0], weights[j], bias[j], logistic))
        activations.append(activation)
        for k in range(layers, -1, -1):
            d_list = []
            if k == len(layers):
                d_list.append(derror(output[:, [i]], activations[i][k]) * dlogistic(x2))
                weights[k] += eta * np.dot(d_list[len(layers) - k], activations[i][k-1].T)
                bias[k]+= eta * d_list[len(layers) - k].sum(axis=1)
            else:
                d_list.append(np.dot(d_list[len(layers) - k - 1].T, weights[k-1]).T * dlogistic(activations[i][k-1]))
                weights[k] += eta * np.dot(d_list[len(layers) - k], activations[i][k-1].T)
                db0 = eta * d_list[len(layers) - k](axis=1)

                
def train_network(input, output, weight_function, num_iters, eta):
    for i in range(num_iters):
        weight_function(input, output, weights, bias, eta)
    return weights, bias
                