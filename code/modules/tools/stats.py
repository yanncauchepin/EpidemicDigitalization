import numpy as np

def part_int(float) :
    if float - int(float) < 0.5 :
        return int(float)
    else :
        return int(float) + 1

def get_random_normal(mean, std) :
    return np.random.normal(mean, std)
