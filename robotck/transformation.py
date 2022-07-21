import numpy as np
import sympy as sp
from typing import List, Union
from .math import MathCK


class Coord_trans:
    @staticmethod
    def mat_rotx(alpha):
        mat = MathCK.matrix(
            [
                [1, 0, 0, 0],
                [0, MathCK.cos(alpha), -MathCK.sin(alpha), 0],
                [0, MathCK.sin(alpha), MathCK.cos(alpha), 0],
                [0, 0, 0, 1],
            ]
        )
        return mat

    @staticmethod
    def mat_roty(beta):
        mat = MathCK.matrix(
            [
                [MathCK.cos(beta), 0, MathCK.sin(beta), 0],
                [0, 1, 0, 0],
                [-MathCK.sin(beta), 0, MathCK.cos(beta), 0],
                [0, 0, 0, 1],
            ]
        )
        return mat

    @staticmethod
    def mat_rotz(theta):
        mat = MathCK.matrix(
            [
                [MathCK.cos(theta), -MathCK.sin(theta), 0, 0],
                [MathCK.sin(theta), MathCK.cos(theta), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )
        return mat

    @staticmethod
    def mat_transl(transl_list: list):
        mat = MathCK.matrix(
            [[1, 0, 0, transl_list[0]], [0, 1, 0, transl_list[1]], [0, 0, 1, transl_list[2]], [0, 0, 0, 1]]
        )
        return mat


class EulerAngle:
    @staticmethod
    def trans2zyx(trans) -> List:
        if MathCK.sqrt(trans[0, 0] ** 2 + trans[1, 0] ** 2) == 0 and -trans[2, 0] == 1:
            b = MathCK.pi() / 2
            a = 0
            r = MathCK.atan2(trans[0, 1], trans[1, 1])
        elif MathCK.sqrt(trans[0, 0] ** 2 + trans[1, 0] ** 2) == 0 and -trans[2, 0] == -1:
            b = -MathCK.pi() / 2
            a = 0
            r = -MathCK.atan2(trans[0, 1], trans[1, 1])
        else:
            b = MathCK.atan2(-trans[2, 0], MathCK.sqrt(trans[0, 0] ** 2 + trans[1, 0] ** 2))
            cb = MathCK.cos(b)
            a = MathCK.atan2(trans[1, 0] / cb, trans[0, 0] / cb)
            r = MathCK.atan2(trans[2, 1] / cb, trans[2, 2] / cb)
        return [a, b, r]

    @staticmethod  # ! not finish todo
    def zyx2trans(alpha, beta, gamma) -> Union[np.matrix, sp.Matrix]:
        ct = Coord_trans
        return MathCK.matmul(ct.mat_rotz(alpha), ct.mat_roty(beta), ct.mat_rotx(gamma))

    @staticmethod  # ! not finish todo
    def xyz2trans(gamma, beta, alpha) -> Union[np.matrix, sp.Matrix]:
        ct = Coord_trans
        return MathCK.matmul(ct.mat_rotx(gamma), ct.mat_roty(beta), ct.mat_rotz(alpha))


class FixedAngle:
    pass
