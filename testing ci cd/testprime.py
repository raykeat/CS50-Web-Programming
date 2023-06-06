#from prime.py file import is_prime function
from prime import is_prime

def test(x,expectedresult):
    if is_prime(x)!=expectedresult:
        print("error")
    else:
        print("right")
