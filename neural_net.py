import numpy as np
import math

np.random.seed(123)

def logistic(x):
    return 1/(1+np.exp(-x))

def d_logistic(x):
    return x*(1-x)

def propagate(inp, w, b, f):
    return f(np.dot(w, inp) + b[:, None])

#+ b[:, None]

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
    print(np.random.randn(num_hidden, input_length))
    weights.append(np.random.randn(num_hidden, input_length))
    bias.append(np.random.randn(num_hidden))
    if layers > 2:
        for i in range(layers-2):
            weights.append(np.random.randn(num_hidden, num_hidden))
            bias.append(np.random.randn(num_hidden))
    weights.append(np.random.randn(output_length, num_hidden))
    bias.append(np.random.randn(outp_length))
    return weights
    
def set_hidden_units(layer, new_hidden):
    if layer == layers:
        print("No hidden units at this layer")
    else:
        bias[layer-1] = np.random.rand(new_hidden)
        weights[layer-1] = np.random.rand(new_hidden, weights[layer-1].shape[1])
        weights[layer] = np.random.rand(weights[layer].shape[1], new_hidden)
    return weights

def update_weights(inp, output, eta):
    activations = []
    new_weights = []
    new_biases = []
    # not sure exactly how the looping while work, but will come back to this
    # and figure it out
    #print(input.shape[1])
    for i in range(inp.shape[1]):
        d_list = []
        # activation = []
        # activation.append(input[:, [i]])
        # for j in range(layers):
            # activation.append(propagate(activation[j], weights[j], bias[j], logistic))
        # print("Input: ", input[:, [i]])
        activation = forward_propagation(inp[:, [i]], logistic)
        for k in range(layers-1, -1, -1):
            if k == layers-1:
                d_list.append(derror(output[:, [i]], activation[k+1]) * d_logistic(activation[k+1]))
                weights[k] += eta * np.dot(d_list[layers - 1 - k], activation[k].T)
                #print("New weights at layer ", str(k), weights[k])
                bias[k]+= eta * d_list[layers -1 - k].sum(axis=1)
                
            else:
                d_list.append(np.dot(d_list[layers - k - 2].T, weights[k+1]).T * d_logistic(activation[k+1]))
                weights[k] += eta * np.dot(d_list[layers - 1 - k], activation[k].T)
                #print("New weights at layer ", str(k), weights[k])
                bias[k] += eta * d_list[layers - 1 - k].sum(axis=1)

def forward_propagation(inp, weight_fn):
    activation = []
    activation.append(inp)
    for j in range(layers):
        #print("activation at layer: ", str(j+1), propagate(activation[j], weights[j], bias[j], weight_fn))
        activation.append(propagate(activation[j], weights[j], bias[j], weight_fn))
    return activation    

def train_network(inp, output, weight_function, num_iters, eta):
    for i in range(num_iters):
        print("Iteration: ", i)
        weight_function(inp, output, eta)
    return weights, bias

def predict_network(inp, weight_function):
    #Z = weight_function(np.dot(weights[0], inp) + bias[0][:, None])
    #Y = weight_function(np.dot(weights[1], Z) + bias[1][:, None])
    # print(Y.shape)
    #return Y


    
    print(forward_propagation(inp, weight_function))
    return forward_propagation(inp, weight_function)[layers]

def get_weights():
    return weights