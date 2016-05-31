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
    s1 = [0, 0, 0]
    s2 = [2, 4, 8]
    s3 = [999, -888, 3]
    p = create_prototype([s1, s2, s3])
    print(p)

if __name__ == '__main__':
    main()