import numpy as np
import audio_utils as au
import math

def prototype(v1, v2):
    return (np.sum(v1)/len(v1)), (np.sum(v2)/len(v2))

def distance(a, b):
    a_ratio = a[1]/a[0]
    b_ratio = b[1]/b[0]
    return abs(a_ratio - b_ratio)/1000

def euclid_d(a, b):
    d = 0
    for i in range(len(a)):
        d += (a[i] - b[i])**2
    return math.sqrt(d)

def predict(example, prototypes):
    ds = []
    for p in prototypes:
        ds.append(euclid_d(example, p))
    return np.argmin(ds)

def shepard_similarity(a, b, distance_fn):
    return math.exp(-distance_fn(a,b))

def prototype_model(test_stimuli, prototypes, distance_fn):
    proto_probs = []
    for i in test_stimuli:
        probs = []
        for j in prototypes:
            num = shepard_similarity(j, i, distance_fn)
            den = 0
            for k in prototypes:
                #print(shepard_similarity(k, i, distance_fn))
                den += shepard_similarity(k, i, distance_fn)
            probs.append(num/den)
        proto_probs.append(probs)
    return proto_probs

def euclid_d_prototype_model(test_stimuli, prototypes, distance_fn):
    proto_probs = []
    for i in test_stimuli:
        probs = []
        for j in prototypes:
            num = shepard_similarity(j, i, distance_fn)
            den = 0
            for k in prototypes:
                #print(shepard_similarity(k, i, distance_fn))
                den += distance_fn(k, i)
            probs.append(num/den)
        proto_probs.append(probs)
    return proto_probs

def create_prototype(stimuli):
    """
    stimuli : a 2-dimensional vector with each row being a stimulus
                stimuli[i][j] is the jth feature of the ith stimulus
    """
    prototype = [0] * len(stimuli[0])
    for i in range(len(stimuli)):
        for j in range(len(stimuli[i])):
            prototype[j] += stimuli[i][j]

    for i in range(len(prototype)):
        prototype[i] /= len(stimuli)

    return prototype

def prediction(probs, instrs):
    predict_list = []
    for i in probs:
        predict_list.append(instrs[np.argmax(i)])
    return predict_list

def frequency(predict_list, desired):
    sum = 0
    for i in predict_list:
        if i == desired:
            sum += 1
    return sum

def freq_list(predict_list, instrs):
    list = [0]*len(instrs)
    for i in range(len(instrs)):
        for j in predict_list:
            if j == instrs[i]:
                list[i] += 1
    return list

def confusion_matrix (probs_list, instrs, outp_length):
    """Gets confusion matrix for a networks output."""
    confusion = np.zeros((outp_length, outp_length))
    for indx in range(len(probs_list)):
        # print(desired[indx])
        i = indx
        # print(actual[indx])
        #print(probs_list[indx])
        for k in probs_list[indx]:
            j = np.argmax(k)
            confusion[i][j] += 1
    return confusion

def print_cc_info(cc, data_length, categories):
    sum1, sum2 = 0, 0
    class_list = []
    for i in range(len(cc)):
        for j in range(len(cc[i])):
            if j == i:
                sum1 += cc[i][j]
                class_list.append(cc[i][j])
            sum2 += cc[i][j]
    print("This model got correct ", sum1, " out of ", sum2, " tests")
    print("which is ", str(sum1/sum2)[:5])
    print(categories)
    for i in range(len(categories)):
        print("For", categories[i], ", This model classified", class_list[i], " out of ", data_length)
        print("which is ", str(class_list[i]/data_length)[:5])

def main():
    print("prototype.py")
    print("This file contains functions to create prototypes")
    print("and uses them to predict novel stimuli.")
    answer = input("Run an example of the prototype model? y/n ")
    if answer == 'y' or answer == 'Y':
        h_data = []
        instrs = ["guitar", "clarinet", "flute", "saxophone", "violin"]
        ind = 0
        for instr in instrs:
            h_data.append(au.fetch_harmonic_rep(instr))

        proto_list = []
        for i in h_data:
            proto_list.append(create_prototype(i[:50])) # use the first 50 examples to create the prototype
        probs_list = []
        for h in h_data:
            probs_list.append(prototype_model(h[50:], proto_list, euclid_d)) # use the rest as testing

        cm = confusion_matrix(probs_list, instrs, 5)
        print_cc_info(cm, len(h[50:]), instrs)

if __name__ == '__main__':
    main()
