"""lagrange
https://github.com/lapets/lagrange

Python library with a basic native implementation of Lagrange
interpolation over finite fields.

"""

import doctest


def inv(a, prime):
    """
    Compute multiplicative inverse modulo a prime.
    """
    return pow(a, prime-2, prime)


def interpolate(points, prime):
    """
    Determine the value at x = 0 given a list of pairs.
    If given a list of integers, assumes they are the
    image of the sequence [1, 2, 3, ...].
    
    >>> interpolate({1: 15, 2: 9, 3: 3}, 17)
    4
    >>> interpolate([(1,15), (2,9), (3,3)], 17)
    4
    >>> interpolate(((1,15), (2,9), (3,3)), 17)
    4
    >>> interpolate({(1,15), (2,9), (3,3)}, 17)
    4
    >>> interpolate([15, 9, 3], 17)
    4
    >>> interpolate(\
        {1: 119182, 2: 11988467, 3: 6052427, 4: 8694701,\
         5: 9050123, 6: 3676518, 7: 558333, 8: 12198248,\
         9: 7344866, 10: 10114014, 11: 2239291, 12: 2515398},\
        15485867)
    123
    >>> interpolate(\
        [119182, 11988467, 6052427, 8694701, 9050123, 3676518,\
         558333, 12198248, 7344866, 10114014, 2239291, 2515398],\
        15485867)
    123
    """
    if type(points) is list and all([type(p) is int for p in points]):
        points = dict(zip(range(1,len(points)+1), points))
    elif type(points) in [list,set,tuple] and\
       len(points) > 0 and\
       all([type(p) in [list,tuple] and len(p) == 2 for p in points]):
        points = dict([tuple(p) for p in points])
    elif type(points) is dict:
        pass
    else:
        raise TypeError("Expecting a list of values, list of points, or a mapping.")

    if type(prime) != int or prime <= 1:
        raise ValueError("Expecting a prime modulus.")

    # Compute the Langrange coefficients at 0.
    coefficients = {}
    for i in range(1, len(points)+1):
      coefficients[i] = 1
      for j in range(1, len(points)+1):
        if j != i:
          coefficients[i] = (coefficients[i] * (0-j) * inv(i-j, prime)) % prime

    value = 0
    for i in range(1, len(points)+1):
      value = (value + points[i] * coefficients[i]) % prime

    return value

lagrange = interpolate # Synonym.

if __name__ == "__main__": 
    doctest.testmod()
