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


def smartAverageMax(x_in, tol):
    avg_raw = np.mean(x_in)
    if len(x_in) > 3:
        indices = np.where(x_in > (1 + tol) * avg_raw)
        x = x_in.copy()
        for i in range(0, len(indices[0])):
            x.__delitem__(indices[0][len(indices[0]) - i - 1])
        avg = np.mean(x)
        return avg
    else:
        return avg_raw


def smartAverageMinMax(x_in, tol):
    avg_raw = np.mean(x_in)
    if len(x_in) > 3:
        indices = np.where(x_in > (1 + tol) * avg_raw)
        x = x_in.copy()
        for i in range(0, len(indices[0])):
            x.__delitem__(indices[0][len(indices[0]) - i - 1])
        indices = np.where(x < (1 - tol) * avg_raw)
        for i in range(0, len(indices[0])):
            x.__delitem__(indices[0][len(indices[0]) - i - 1])
        avg = np.mean(x)
        return avg
    else:
        return avg_raw


def meanTol(x_in: list, tol: float):
    x_clean = [k for k in x_in if str(k) != 'nan']

    mean = np.mean(x_clean).item()
    if len(x_clean) < 3:
        return float(mean)
    else:
        x = np.array(x_clean)
        dev_abs = np.abs(x - mean)
        dev_rel = dev_abs / mean
        withintolerance = np.greater(tol, dev_rel).tolist()
        indices = [i for i, x in enumerate(withintolerance) if x]
        if len(indices) < 3:
            return float(mean)
        else:
            x_new = x[indices]
            meanWithinTol = np.mean(x_new).item()
            return float(meanWithinTol)


def maxList(L, value):
    if type(L) is list:
        CondBool = np.array(L) < value

        if type(CondBool) is not list:
            CondBool = [CondBool]

        indexes = [i for i, x in enumerate(CondBool) if x]

        for k in indexes:
            L[k] = value

        return L
    elif type(L) is int:
        return max(L, value)

def angleVertical(dx, dy):
    a = 0
    if dx == 0:
        if dy > 0:
            a = np.pi
        else:
            a = 0
    elif dx > 0:
        if dy > 0:
            a = -np.arctan(dx/dy) + np.pi
        elif dy < 0:
            a = -np.arctan(dx/dy)
        else:
            a = np.pi / 2
    elif dx < 0:
        if dy > 0:
            a = -np.arctan(dx/dy) + np.pi
        elif dy < 0:
            a = 2 * np.pi - np.arctan(dx/dy)
        else:
            a = np.pi * 1.5

    return a
