import numpy as np
import math

def prototype(v1, v2):
    return((np.sum(v2)/len(v2))/(np.sum(v1)/len(v1)))

def distance(a, b):
    a_ratio = a[1]/a[0]
    b_ratio = b[1]/b[0]
    return(abs(a_ratio - b_ratio))

def shepard_similarity(a, b):
    return math.exp(-distance(a,b))

#def prototype_model(test_stimuli, prototypes):
    probs = []
    for i in range (len(test_stimuli)):
        for j in prototypes:
            num = shepard_similarity(
                    
    