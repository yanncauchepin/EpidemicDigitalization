import numpy as np

def partInt(float) :
    if float - int(float) < 0.5 :
        return int(float)
    else :
        return int(float) + 1

def getFoldedNormal(mean, std) :
    return np.random.normal(mean, std)
