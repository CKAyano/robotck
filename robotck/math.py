from typing import Tuple
import numpy as np
import sympy as sp


MODULE_HANDLER = {"numpy": np, "sympy": sp}


class MathCK:
    __type = MODULE_HANDLER["numpy"]

    @staticmethod
    def set_type(type: str):
        if type != "numpy" and type != "sympy":
            raise TypeError("type should be np.matrix or sp.Matrix")

        MathCK.__type = MODULE_HANDLER[type]

    @staticmethod
    def get_type():
        return MathCK.__type

    @staticmethod
    def is_type(type: str):
        if MathCK.__type == MODULE_HANDLER[type]:
            return True
        return False

    @staticmethod
    def pi():
        return MathCK.__type.pi

    @staticmethod
    def matrix(arr):
        if MathCK.__type == MODULE_HANDLER["sympy"]:
            return MathCK.__type.Matrix(arr)
        return MathCK.__type.array(arr)

    @staticmethod
    def hstack(elms: Tuple):
        if MathCK.__type == MODULE_HANDLER["sympy"]:
            return sp.Matrix.hstack(*elms)
        return np.hstack(elms)

    @staticmethod
    def cos(angle):
        return MathCK.__type.cos(angle)

    @staticmethod
    def sin(angle):
        return MathCK.__type.sin(angle)

    @staticmethod
    def sqrt(num):
        return MathCK.__type.sqrt(num)

    @staticmethod
    def atan2(num1, num2):
        if MathCK.__type == MODULE_HANDLER["sympy"]:
            return MathCK.__type.atan2(num1, num2)
        return MathCK.__type.arctan2(num1, num2)

    @staticmethod
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
            if MathCK.__type == MODULE_HANDLER["sympy"]:
                res = res * mat
            else:
                res = res @ mat
        return res
