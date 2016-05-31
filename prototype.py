import numpy as np
import math

def prototype(v1, v2):
    return (np.sum(v1)/len(v1)), (np.sum(v2)/len(v2)) 

def distance(a, b):
    a_ratio = a[1]/a[0]
    b_ratio = b[1]/b[0]
    return abs(a_ratio - b_ratio)/1000 

def shepard_similarity(a, b):
    return math.exp(-distance(a,b))

def prototype_model(test_stimuli, prototypes):
    proto_probs = []
    for i in test_stimuli:
        probs = []
        for j in prototypes:
            num = shepard_similarity(j, i)
            den = 0
            for k in prototypes:
                den += shepard_similarity(k, i)
            probs.append(num/den)
        proto_probs.append(probs)
    return proto_probs
                    
    