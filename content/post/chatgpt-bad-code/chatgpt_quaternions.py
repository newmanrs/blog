import math
import random
import numpy as np

def method_A():  # Chat GPT
    x0 = random.random()
    x1 = random.random()
    x2 = random.random()
    x3 = random.random()

    r = np.sqrt(x0*x0 + x1*x1 + x2*x2 + x3*x3)
    return [x0/r, x1/r, x2/r, x3/r]



def method_B():  # Chat GPT
    # Generate random numbers for the quaternion values
    q = [random.uniform(-1, 1) for i in range(4)]
    # Normalize the quaternion
    return q / np.linalg.norm(q)


def method_C():  # Chat GPT
    # Generate three independent random variables from the standard normal distribution
    xi1, xi2, xi3 = np.random.normal(size=3)

    # Compute the remaining component of the quaternion
    q0 = np.sqrt(1 - xi1**2 - xi2**2 - xi3**2)

    # Return the quaternion as a NumPy array
    return np.array([q0, xi1, xi2, xi3])

def method_D():  # Chat GPT
    x1 = random.uniform(0, 1)
    x2 = random.uniform(0, 1)
    x3 = random.uniform(0, 1)
    r1 = math.sqrt(1 - x1)
    r2 = math.sqrt(x1)
    t1 = 2 * math.pi * x2
    t2 = 2 * math.pi * x3
    return (math.sin(t1) * r1, math.cos(t1) * r1, math.sin(t2) * r2, math.cos(t2) * r2)

def method_E():  # By me (newmanrs)
    q = np.random.normal(size=(4,))
    return q / np.linalg.norm(q)

def test_naive(funcs):
    d = dict()
    for func in funcs:
        s = np.mean(np.stack([np.asarray(func()) for _ in range(100000)]),axis=0)
        print(func.__name__, s)

if __name__ == '__main__':
    funcs = [method_A, method_B, method_C, method_D, method_E]
    test_naive(funcs)



