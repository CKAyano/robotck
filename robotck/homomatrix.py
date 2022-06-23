from typing import Union
import numpy as np
import sympy as sp
from .transformation import EulerAngle


class HomoMatrix:
    def __init__(self, matrix: Union[np.ndarray, np.matrix, sp.Matrix]) -> None:
        is_ndarray = isinstance(matrix, np.ndarray)
        is_ndmatrix = isinstance(matrix, np.matrix)
        is_spmatrix = isinstance(matrix, sp.Matrix)
        if is_ndarray or is_ndmatrix or is_spmatrix:
            pass
        else:
            raise TypeError("input type is wrong")

        self._error_raising(matrix)

        if isinstance(matrix, np.ndarray):
            matrix = np.asmatrix(matrix)

        self.matrix = matrix
        self.axis_matrix = None

    def _error_raising(self, trans):
        if trans.shape[0] != 4 or trans.shape[1] != 4:
            raise RuntimeError("Transfer matrice must 3x3")

    def __repr__(self) -> str:
        if isinstance(self.matrix, np.matrix):
            return "Trans(np.matrix)"
        if isinstance(self.matrix, sp.Matrix):
            return "Trans(sp.Matrix)"

    def __str__(self) -> str:
        return f"{self.matrix}"

    def __getitem__(self, key):
        return self.matrix[key]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def __eq__(self, o: object) -> bool:
        if np.all(self.matrix == o.trans):
            return True
        return False

    @property
    def coord(self):
        return self.matrix[:3, 3]

    @coord.setter
    def coord(self, transl):
        if not isinstance(transl, self.matrix):
            raise TypeError("input type is wrong")
        self.matrix[:3, 3] = transl

    @property
    def rot(self):
        return self.matrix[:3, :3]

    @rot.setter
    def rot(self, rot):
        if not isinstance(rot, self.matrix):
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
