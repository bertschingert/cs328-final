import numpy as np
import audio_utils as au
import math

np.random.seed(123)

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
        bias[layer-1] = np.random.randn(new_hidden)
        weights[layer-1] = np.random.randn(new_hidden, weights[layer-1].shape[1])
        weights[layer] = np.random.randn(weights[layer].shape[1], new_hidden)
    return weights

def update_weights(inp, output, eta):
    activations = []
    new_weights = []
    new_biases = []
    for i in range(inp.shape[1]):
        d_list = []
        activation = forward_propagation(inp[:, [i]], logistic)
        for k in range(layers-1, -1, -1):
            if k == layers-1:
                d_list.append(derror(output[:, [i]], activation[k+1]) * d_logistic(activation[k+1]))
                weights[k] += eta * np.dot(d_list[layers - 1 - k], activation[k].T)
                bias[k]+= eta * d_list[layers -1 - k].sum(axis=1)

            else:
                d_list.append(np.dot(d_list[layers - k - 2].T, weights[k+1]).T * d_logistic(activation[k+1]))
                weights[k] += eta * np.dot(d_list[layers - 1 - k], activation[k].T)
                bias[k] += eta * d_list[layers - 1 - k].sum(axis=1)

def forward_propagation(inp, weight_fn):
    activation = []
    activation.append(inp)
    for j in range(layers):
        activation.append(propagate(activation[j], weights[j], bias[j], weight_fn))
    return activation

def train_network(inp, output, weight_function, num_iters, eta):
    for i in range(num_iters):
        if i%10 == 0:
            print("Iteration:", i)
        weight_function(inp, output, eta)
    return weights, bias

def predict_network(inp, weight_function):
    return forward_propagation(inp, weight_function)[layers]

def get_weights():
    return weights

def main():
    print("neural_net.py")
    print("This file contains the functions to train a neural network")
    print("and to test the network on novel stimuli.")
    answer = input("Run a test computation of the neural net? y/n ")
    if answer == 'y' or answer == 'Y':
        f_data = []
        instrs = ["guitar", "clarinet", "flute", "saxophone", "violin"]
        for instr in instrs:
            f_data.append(au.fetch_nflux_rep(instr))

        f_inp = []
        f_outputs = []
        print("creating training data...")
        for i in range(50):
            for j in range(5):
                f_output = [0]*5
                f_output[j] = 1
                f_outputs.append(f_output)
                f_inp.append(np.array(f_data[j][i]))

        f_inp = np.array(f_inp)
        f_out = np.array(f_outputs)

        initialize_network(f_inp.T.shape[0], f_out.T.shape[0], 3, 5)
        set_hidden_units(1, 10)
        print("training the network")
        train_network(f_inp.T, f_out.T, update_weights, 300, 0.01)
        print("**************************")
        print("predicting the network:")
        real = predict_network(f_inp.T, logistic)
        cm = au.confusion_matrix(real.T, f_out, f_out.T.shape[0])
        print(cm)
        au.print_cc_info(cm, 50, instrs)

if __name__ == '__main__':
    main()
