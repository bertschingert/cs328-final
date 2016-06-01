import numpy as np
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

def main():
    print("prototype.py")
    print("This file contains functions to create prototypes")
    print("and uses them to predict novel stimuli.")

if __name__ == '__main__':
    main()
