import numpy as np
import sympy as sp


class MathCK:
    __type = np

    @staticmethod
    def set_type(type):
        if type != np and type != sp:
            raise TypeError("type should be np.matrix or sp.Matrix")

        MathCK.__type = type

    @staticmethod
    def pi():
        return MathCK.__type.pi

    @staticmethod
    def matrix(array):
        if MathCK.__type == np:
            return MathCK.__type.matrix(array)
        if MathCK.__type == sp:
            return MathCK.__type.Matrix(array)

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
        if MathCK.__type == np:
            return MathCK.__type.arctan2(num1, num2)
        if MathCK.__type == sp:
            return MathCK.__type.atan2(num1, num2)
