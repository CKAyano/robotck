from typing import Optional, Union
from typing_extensions import Self
import numpy as np
import sympy as sp

from robotck.math import MathCK
from .transformation import EulerAngle
from .expressionHandler import ExpressionHandler


class HomoMatrix:
    def __init__(self, matrix: Union[np.ndarray, sp.Matrix]) -> None:
        is_ndarray = isinstance(matrix, np.ndarray)
        # is_ndmatrix = isinstance(matrix, np.matrix)
        is_spmatrix = isinstance(matrix, sp.Matrix)
        # if is_ndarray or is_ndmatrix or is_spmatrix:
        if is_ndarray or is_spmatrix:
            pass
        else:
            raise TypeError("input type is wrong")

        if matrix.shape[0] != 4 or matrix.shape[1] != 4:
            raise RuntimeError("Transfer matrice must 4x4")

        # if isinstance(matrix, np.ndarray):
        #     matrix = np.asmatrix(matrix)

        self.matrix = matrix
        self.axis_matrix: Optional[Union[np.ndarray, sp.Matrix]] = None

    def __repr__(self) -> str:
        if isinstance(self.matrix, np.ndarray):
            return "HomoMatrix(np.ndarray)"
        if isinstance(self.matrix, sp.Matrix):
            return "HomoMatrix(sp.Matrix)"
        return repr(self.matrix)

    def __str__(self) -> str:
        return f"{self.matrix}"

    def __getitem__(self, key):
        return self.matrix[key]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def __eq__(self, o: Self) -> bool:
        if np.all(self.matrix == o.matrix):
            return True
        return False

    @property
    def coord(self):
        return self.matrix[0:3, 3]

    @coord.setter
    def coord(self, transl):
        if not isinstance(transl, type(self.matrix)):
            raise TypeError("input type is wrong")
        self.matrix[0:3, 3] = transl

    @property
    def rot(self):
        return self.matrix[0:3, 0:3]

    @rot.setter
    def rot(self, rot):
        if not isinstance(rot, type(self.matrix)):
            raise TypeError("input type is wrong")

        if rot.shape[0] != 3 or rot.shape[1] != 3:
            raise RuntimeError("rotation matrice must 3x3")

        self.matrix[:3, :3] = rot

    @property
    def zyxeuler(self):
        return EulerAngle.trans2zyx(self.matrix)

    @property
    def xyzfixed(self):
        return EulerAngle.trans2zyx(self.matrix)

    def distance(self, other):
        if isinstance(other, HomoMatrix):
            np_self = self.coord.squeeze()
            np_other = other.coord.squeeze()
            return np.sqrt(np.sum(np.square(np_self - np_other)))
        if isinstance(other, list):
            np_self = self.coord.squeeze()
            np_other = np.array(other)
            return np.sqrt(np.sum(np.square(np_self - np_other)))
        return NotImplemented

    def round(self, n) -> None:
        _round_homoMatirx(self, n)

    def float_to_pi(self) -> None:
        _convert_homomatrix_float_to_pi(self)

    def get_coord_list(self):
        if MathCK.is_type("sympy"):
            temp = sp.matrix2numpy(self.coord).squeeze()
            return [temp[0], temp[1], temp[2]]
        temp = self.coord.squeeze()
        return [temp[0], temp[1], temp[2]]


def _round_homoMatirx(homoMatrix: HomoMatrix, n):
    homoMatrix.matrix = ExpressionHandler._round_expr(homoMatrix.matrix, n)
    homoMatrix.axis_matrix = ExpressionHandler._round_expr(homoMatrix.axis_matrix, n)


def _convert_homomatrix_float_to_pi(homoMatrix: HomoMatrix):
    homoMatrix.matrix = ExpressionHandler._convert_float_to_pi(homoMatrix.matrix)
    homoMatrix.axis_matrix = ExpressionHandler._convert_float_to_pi(homoMatrix.axis_matrix)
