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
        bias[layer-1] = np.random.rand(new_hidden)
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
        d_list = []
        # activation = []
        # activation.append(input[:, [i]])
        # for j in range(layers):
            # activation.append(propagate(activation[j], weights[j], bias[j], logistic))
        activation = forward_propagation(input[:, [i]], logistic)
        for k in range(layers-1, -1, -1):
            if k == layers-1:
                d_list.append(derror(output[:, [i]], activation[k+1]) * d_logistic(activation[k+1]))
                weights[k] += eta * np.dot(d_list[layers - 1 - k], activation[k].T)
                bias[k]+= eta * d_list[layers -1 - k].sum(axis=1)
                
            else:
                d_list.append(np.dot(d_list[layers - k - 2].T, weights[k+1]).T * d_logistic(activation[k+1]))
                weights[k] += eta * np.dot(d_list[layers - 1 - k], activation[k].T)
                bias[k] += eta * d_list[layers - 1 - k].sum(axis=1)

def forward_propagation(input, weight_fn):
    activation = []
    activation.append(input)
    for j in range(layers):
        activation.append(propagate(activation[j], weights[j], bias[j], weight_fn))
    print(activation)
    return activation    
def train_network(input, output, weight_function, num_iters, eta):
    for i in range(num_iters):
        print("Iteration: ", i)
        weight_function(input, output, eta)
    return weights, bias

def predict_network(input, weight_function):
    print(forward_propagation(input, weight_function))
    return forward_propagation(input, weight_function)[layers]

def get_weights():
    return weights