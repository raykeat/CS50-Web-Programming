import math
from math import sqrt, ceil

def is_prime(x):
    if x<2:
        return False
    elif x==2:
        return True
    else:
        for i in range(3,int(ceil(sqrt(x)))+1):
            if x%i==0:
                return False
        return True
    