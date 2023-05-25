def logistic(x):
    return 1.0/(1 + np.exp(-x))

def relu(x):
    return max(x,0)

def leaky_relu(x):
    if x > 0:
        return x
    else:
        return 0.1*x

import numpy as np

def elu(x):
    if x > 0:
        return x
    else:
        return (np.exp(x)-1)
    
def arctanplusone(x):
    return np.arctan(x)+x

def logistic_deriv(x):
    return logistic(x) * (1 - logistic(x))

def relu_deriv(x):
    if relu(x) > 0:
        return 1
    else:
        return 0

def leaky_relu_deriv(x):
    if x > 0:
        return 1
    else:
        return 0.1

def elu_deriv(x):
    if x > 0:
        return 1
    else:
        return np.exp(x)

def arctanplusone_deriv(x):
    return (x**2+2)/(x**2+1)