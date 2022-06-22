import numpy as np
import scipy as sp
from typing import List, Union


class Coord_trans:
    @staticmethod
    def mat_rotx(alpha):
        mat = _MathCK.matrix(
            [
                [1, 0, 0, 0],
                [0, _MathCK.cos(alpha), -_MathCK.sin(alpha), 0],
                [0, _MathCK.sin(alpha), _MathCK.cos(alpha), 0],
                [0, 0, 0, 1],
            ]
        )
        return mat

    @staticmethod
    def mat_roty(beta):
        mat = _MathCK.matrix(
            [
                [_MathCK.cos(beta), 0, _MathCK.sin(beta), 0],
                [0, 1, 0, 0],
                [-_MathCK.sin(beta), 0, _MathCK.cos(beta), 0],
                [0, 0, 0, 1],
            ]
        )
        return mat

    @staticmethod
    def mat_rotz(theta):
        mat = _MathCK.matrix(
            [
                [_MathCK.cos(theta), -_MathCK.sin(theta), 0, 0],
                [_MathCK.sin(theta), _MathCK.cos(theta), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )
        return mat

    @staticmethod
    def mat_transl(transl_list: list):
        mat = _MathCK.matrix(
            [[1, 0, 0, transl_list[0]], [0, 1, 0, transl_list[1]], [0, 0, 1, transl_list[2]], [0, 0, 0, 1]]
        )
        return mat


class EulerAngle:
    @staticmethod
    def trans2zyx(trans) -> List:
        if _MathCK.sqrt(trans[0, 0] ** 2 + trans[1, 0] ** 2) == 0 and -trans[2, 0] == 1:
            b = _MathCK.pi / 2
            a = 0
            r = _MathCK.atan2(trans[0, 1], trans[1, 1])
        elif _MathCK.sqrt(trans[0, 0] ** 2 + trans[1, 0] ** 2) == 0 and -trans[2, 0] == -1:
            b = -_MathCK.pi / 2
            a = 0
            r = -_MathCK.atan2(trans[0, 1], trans[1, 1])
        else:
            b = _MathCK.atan2(-trans[2, 0], _MathCK.sqrt(trans[0, 0] ** 2 + trans[1, 0] ** 2))
            cb = _MathCK.cos(b)
            a = _MathCK.atan2(trans[1, 0] / cb, trans[0, 0] / cb)
            r = _MathCK.atan2(trans[2, 1] / cb, trans[2, 2] / cb)
        return [a, b, r]

    @staticmethod  # ! not finish todo
    def zyx2trans(alpha, beta, gamma) -> Union[np.matrix, sp.Matrix]:
        ct = Coord_trans
        return ct.mat_rotz(alpha) * ct.mat_roty(beta) * ct.mat_rotx(gamma)

    @staticmethod  # ! not finish todo
    def xyz2trans(gamma, beta, alpha) -> Union[np.matrix, sp.Matrix]:
        ct = Coord_trans
        return ct.mat_rotx(gamma) * ct.mat_roty(beta) * ct.mat_rotz(alpha)


class FixedAngle:
    pass


class _MathCK:
    __type = np

    @staticmethod
    def set_type(type):
        if type != np and type != sp:
            raise TypeError("type should be np.matrix or sp.Matrix")

        _MathCK.__type = type

    @staticmethod
    def pi():
        return _MathCK.__type.pi

    @staticmethod
    def matrix(array):
        if _MathCK.__type == np:
            return _MathCK.__type.matrix(array)
        if _MathCK.__type == sp:
            return _MathCK.__type.Matrix(array)

    @staticmethod
    def cos(angle):
        return _MathCK.__type.cos(angle)

    @staticmethod
    def sin(angle):
        return _MathCK.__type.sin(angle)

    @staticmethod
    def sqrt(num):
        return _MathCK.__type.sqrt(num)

    @staticmethod
    def atan2(num1, num2):
        if _MathCK.__type == np:
            return _MathCK.__type.arctan2(num1, num2)
        if _MathCK.__type == sp:
            return _MathCK.__type.atan2(num1, num2)
