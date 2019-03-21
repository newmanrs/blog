import itertools
import time
import numpy as np

class Timer:

    def __init__(self,name=None,verbose=True):
        self.name = name
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time() # - 3.7 only for - time.perf_counter_ns()
        return self

    def __exit__(self, *args):
        self.end = time.time() # - 3.7 only for time.perf_counter_ns()
        self.interval = self.end - self.start
        if(self.verbose):
            if self.name is not None:
                print("Timer {} elapsed {:.4f}s".format(self.name,self.interval))
            else:
                print("Timer elapsed {:.4f}s".format(self.interval))

def integer_to_digit_array(value):
    """ Convert integer into digit array """

    #List comprehension
    return [int(i) for i in list(str(value))]

    #Hideous C-like math
    #l = np.log10(value)+1
    #a = np.zeros(l,dtype=np.uint8)
    #i = 0
    #while value > 1:
    #    a[l-1-i] = value % 10
    #    value /= 10
    #    i+=1
    #return a

def digit_array_to_integer(value):
    # Python's int/char/string expressions surprisingly efficient
    return int(''.join([str(v) for v in value]))


    # C-style summation w/o abusing string - way too slow
    #n = len(value)
    #tmp = 0
    #for k in range(n):
    #    tmp += value[k] * 10**(n-1-k)
    #return tmp

    # Numpy vectorization - Also slow.
    #v = np.asarray(value)
    #p = 10**np.linspace(len(value)-1, 0, len(value)).astype(int)
    #return np.sum(v * p)



def get_next_largest_permutation(value):
    ## TODO: converting to/from digit array on enter/exit of function is a tad inefficient
    ## for the generator-wrapped version (should store value as integer array)

    a = integer_to_digit_array(value)
    n = len(a)
    # Scan from right to left first looking for a favorable swap
    leftpiv = None
    for i in range(n-2,-1,-1): #for n=4, we iterate i, 2,1,0
        #compare i, i+1.
        if a[i] < a[i+1]:
            leftpiv = i
            break

    if leftpiv is None: #Case of no swap (number is sorted descending)
        return None

    # Find smallest "larger" number than the pivot point to the right side
    leftv = a[leftpiv]
    rightv = 9      #Initialize as largest
    rightpiv = leftpiv+1
    for i in range(leftpiv+1,n):
        if a[i] > leftv and a[i] <= rightv:
            rightpiv = i
            rightv = a[i]


    #Swap time
    tmp = a[rightpiv]
    a[rightpiv] = a[leftpiv]
    a[leftpiv]  = tmp

    #sort right of left piv
    a[leftpiv+1:] = sorted(a[leftpiv+1:])
    return digit_array_to_integer(a)

def iter_next_largest_permutation(value):
    """ generator variant """
    next_value = get_next_largest_permutation(value)
    while next_value is not None:
        yield next_value
        next_value = get_next_largest_permutation(next_value)

#def test_same_as_brute_force():
    """ test against brute force from itertools module """


if __name__ == "__main__":

    start = 123454321 

    """ our codepath """
    with Timer("Our iterator") as t:
        larger_ps = [i for i in iter_next_largest_permutation(start)]

    #print("We found:")
    #print(larger_ps)

    """ itertools brute force """
    with Timer("Naive use of iter tools") as t:
        g = itertools.permutations(integer_to_digit_array(start))
        all_p = [digit_array_to_integer(p) for p in g]
        all_p = np.unique(np.asarray(all_p)) #Repeated digits are treated as "distinguishable" by this module
        larger_ps_itertools = sorted(all_p[all_p > start])

    #print("Itertools: ")
    #print(larger_ps_itertools)

    #Sanity check
    if len(larger_ps) != len(larger_ps_itertools):
        raise ValueError
    for a,b in zip(larger_ps, larger_ps_itertools):
        if a != b:
            raise ValueError("mismatch in values computed via different methods")
