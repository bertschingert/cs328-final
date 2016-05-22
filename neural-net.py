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

def initialize_network(inp_length, outp_length, layers, num_hidden):
    global layers = layers
    weights = []
    bias = []
    weights.append(np.random.rand(num_hidden, inp_length))
    bias.append(np.random.rand(num_hidden))
    if layers > 3:
        for i in range(layers-2):
            weights.append(np.random.rand(num_hidden, num_hidden))
            bias.append(np.random.rand(num_hidden))
    weights.append(np.random.rand(outp_length, num_hidden))
    bias.append(np.random.rand(outp_length))
    global weights = tuple(weights)
    global bias = tuple(bias)
    return weights
    
def set_hidden_units(layer, num_hidden):
    weights[layer-1] = np.random.rand(num_hidden, num_hidden)
    return weights

def update_weights(input, output, eta):
    activations 
    # not sure exactly how the looping while work, but will come back to this
    # and figure it out
    for i in range(input.shape[1]):
        x0 = x[:, [i]]
        for i in range(layers):
            
                
                
def train_network(input, output, weight_function, num_iters, eta):
    for i in range(num_iters):
        weight_function(input, output, weights, bias, eta)
    return weights, bias
                
