from typing import Any, List
from .math import MathCK


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


def mat_transl(transl_list: list):
    mat = MathCK.matrix(
        [[1, 0, 0, transl_list[0]], [0, 1, 0, transl_list[1]], [0, 0, 1, transl_list[2]], [0, 0, 0, 1]]
    )
    return mat


def rot_rotx(alpha):
    mat = MathCK.matrix(
        [
            [1, 0, 0],
            [0, MathCK.cos(alpha), -MathCK.sin(alpha)],
            [0, MathCK.sin(alpha), MathCK.cos(alpha)],
        ]
    )
    return mat


def rot_roty(beta):
    mat = MathCK.matrix(
        [
            [MathCK.cos(beta), 0, MathCK.sin(beta)],
            [0, 1, 0],
            [-MathCK.sin(beta), 0, MathCK.cos(beta)],
        ]
    )
    return mat


def rot_rotz(theta):
    mat = MathCK.matrix(
        [
            [MathCK.cos(theta), -MathCK.sin(theta), 0],
            [MathCK.sin(theta), MathCK.cos(theta), 0],
            [0, 0, 1],
        ]
    )
    return mat


def trans2zyx_euler(trans) -> List:
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


def trans2zyz_euler(trans) -> List:
    if MathCK.sqrt(trans[2, 0] ** 2 + trans[2, 1] ** 2) == 0 and trans[2, 2] == 1:
        b = 0
        a = 0
        r = MathCK.atan2(-trans[0, 1], trans[0, 0])
    elif MathCK.sqrt(trans[2, 0] ** 2 + trans[2, 1] ** 2) == 0 and trans[2, 2] == -1:
        b = MathCK.pi()
        a = 0
        r = MathCK.atan2(trans[0, 1], -trans[0, 0])
    else:
        b = MathCK.atan2(MathCK.sqrt(trans[2, 0] ** 2 + trans[2, 1] ** 2), trans[2, 2])
        sb = MathCK.sin(b)
        a = MathCK.atan2(trans[1, 2] / sb, trans[0, 2] / sb)
        r = MathCK.atan2(trans[2, 1] / sb, -trans[2, 0] / sb)
    return [a, b, r]


def trans2zyz_euler_sec(trans) -> List:
    if MathCK.sqrt(trans[2, 0] ** 2 + trans[2, 1] ** 2) == 0 and trans[2, 2] == 1:
        b = 0
        a = 0
        r = MathCK.atan2(-trans[0, 1], trans[0, 0])
    elif MathCK.sqrt(trans[2, 0] ** 2 + trans[2, 1] ** 2) == 0 and trans[2, 2] == -1:
        b = MathCK.pi()
        a = 0
        r = MathCK.atan2(trans[0, 1], -trans[0, 0])
    else:
        b = -MathCK.atan2(MathCK.sqrt(trans[2, 0] ** 2 + trans[2, 1] ** 2), trans[2, 2])
        sb = MathCK.sin(b)
        a = MathCK.atan2(trans[1, 2] / sb, trans[0, 2] / sb)
        r = MathCK.atan2(trans[2, 1] / sb, -trans[2, 0] / sb)
    return [a, b, r]


def trans2xyz_fixed(trans) -> List:
    return trans2zyx_euler(trans)


def trans2zyz_fixed(trans) -> List:
    return trans2zyz_euler(trans)


def zyx_euler2trans(alpha, beta, gamma) -> Any:
    return MathCK.matmul(mat_rotz(alpha), mat_roty(beta), mat_rotx(gamma))


def zyz_euler2trans(alpha, beta, gamma):
    return MathCK.matmul(mat_rotz(alpha), mat_roty(beta), mat_rotz(gamma))


def xyz_fixed2trans(gamma, beta, alpha):
    return zyx_euler2trans(alpha, beta, gamma)


def zyz_fixed2trans(alpha, beta, gamma):
    return zyz_euler2trans(gamma, beta, alpha)
