import numpy as np
import scipy.signal
import scipy.optimize


def poly2(x, a, b, c):  # TODO: remove
    return a + b * x + c * np.power(x, 2)


def poly3(x, a, b, c, d):  # TODO: remove
    return a + b * x + c * np.power(x, 2) + d * np.power(x, 3)


def poly6(x, a, b, c, d, e, f):  # TODO: remove
    return a + b * x + c * np.power(x, 2) + d * np.power(x, 3) + e * np.power(x, 4) + f * np.power(x, 5)


def findIntersection(fun1, fun2, x0):
    return scipy.optimize.fsolve(lambda x: fun1(x) - fun2(x), x0)


def polyVal(x, *args):
    if isinstance(args[0], np.ndarray):
        c = args[0]
    else:
        c = args

    r = 0

    for i in range(0, len(c)):
        r += c[i] * np.power(x, i)

    return r