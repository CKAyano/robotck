from typing import Tuple
import numpy as np
import sympy as sp


MODULE_HANDLER = {"numpy": np, "sympy": sp}


class __Type:
    __type = MODULE_HANDLER["numpy"]


def pi():
    return __Type.__type.pi


def set_type(type: str):
    if type != "numpy" and type != "sympy":
        raise TypeError("type should be np.matrix or sp.Matrix")
    __Type.__type = MODULE_HANDLER[type]


def get_type():
    return __Type.__type


def is_type(type: str):
    if __Type.__type == MODULE_HANDLER[type]:
        return True
    return False


def matrix(arr):
    if __Type.__type == MODULE_HANDLER["sympy"]:
        return __Type.__type.Matrix(arr)
    return __Type.__type.array(arr)


def hstack(elms: Tuple):
    if __Type.__type == MODULE_HANDLER["sympy"]:
        return sp.Matrix.hstack(*elms)
    return np.hstack(elms)


def cos(angle):
    return __Type.__type.cos(angle)


def sin(angle):
    return __Type.__type.sin(angle)


def sqrt(num):
    return __Type.__type.sqrt(num)


def atan2(num1, num2):
    if __Type.__type == MODULE_HANDLER["sympy"]:
        return __Type.__type.atan2(num1, num2)
    return __Type.__type.arctan2(num1, num2)


def matmul(*mats: np.ndarray | sp.Matrix) -> np.ndarray | sp.Matrix:
    is_all_ndarray = all(isinstance(i, np.ndarray) for i in mats)
    is_all_spmatrix = all(isinstance(i, sp.Matrix) for i in mats)
    if not is_all_ndarray and not is_all_spmatrix:
        raise TypeError("argument must the same type")
    res = None
    for i, mat in enumerate(mats):
        if i == 0:
            res = mat
            continue
        if __Type.__type == MODULE_HANDLER["sympy"]:
            res = res * mat
        else:
            res = res @ mat
    return res
