from typing import List, Optional, Union
import numpy as np
import copy
from Package.NelderMeadSimplex import simplex
from enum import Enum, auto
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


class Type_angle(Enum):
    RAD = auto()
    DEG = auto()


class Type_DH(Enum):
    STANDARD = auto()
    MODIFIED = auto()


class Coord_trans:
    @staticmethod
    def mat_rotx(alpha):
        mat = np.array(
            [
                [1, 0, 0, 0],
                [0, np.cos(alpha), -np.sin(alpha), 0],
                [0, np.sin(alpha), np.cos(alpha), 0],
                [0, 0, 0, 1],
            ]
        )
        return mat

    @staticmethod
    def mat_roty(beta):
        mat = np.array(
            [
                [np.cos(beta), 0, np.sin(beta), 0],
                [0, 1, 0, 0],
                [-np.sin(beta), 0, np.cos(beta), 0],
                [0, 0, 0, 1],
            ]
        )
        return mat

    @staticmethod
    def mat_rotz(theta):
        mat = np.array(
            [
                [np.cos(theta), -np.sin(theta), 0, 0],
                [np.sin(theta), np.cos(theta), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )
        return mat

    @staticmethod
    def mat_transl(transl_list: list):
        mat = np.array(
            [[1, 0, 0, transl_list[0]], [0, 1, 0, transl_list[1]], [0, 0, 1, transl_list[2]], [0, 0, 0, 1]]
        )
        return mat


class Euler_trans:
    @staticmethod
    def trans2zyx(trans):
        if np.sqrt(trans[0, 0] ** 2 + trans[1, 0] ** 2) == 0 and -trans[2, 0] == 1:
            b = np.pi / 2
            a = 0
            r = np.arctan2(trans[0, 1], trans[1, 1])
        elif np.sqrt(trans[0, 0] ** 2 + trans[1, 0] ** 2) == 0 and -trans[2, 0] == -1:
            b = -np.pi / 2
            a = 0
            r = -np.arctan2(trans[0, 1], trans[1, 1])
        else:
            b = np.arctan2(-trans[2, 0], np.sqrt(trans[0, 0] ** 2 + trans[1, 0] ** 2))
            cb = np.cos(b)
            a = np.arctan2(trans[1, 0] / cb, trans[0, 0] / cb)
            r = np.arctan2(trans[2, 1] / cb, trans[2, 2] / cb)
        return [r, b, a]

    @staticmethod  # ! not finish todo
    def zyx2trans(alpha, beta, gamma):
        ct = Coord_trans
        return ct.mat_rotz(alpha).dot(ct.mat_roty(beta).dot(ct.mat_rotx(gamma)))

    @staticmethod  # ! not finish todo
    def xyz2trans(gamma, beta, alpha):
        ct = Coord_trans
        return ct.mat_rotx(gamma).dot(ct.mat_roty(beta).dot(ct.mat_rotz(alpha)))


class Trans:
    def __init__(self, trans: np.ndarray) -> None:
        try:
            if trans.ndim != 2 or trans.shape[0] != 4 or trans.shape[1] != 4:
                raise RuntimeError("Transfer matrice must 3x3")
        except RuntimeError as e:
            print(repr(e))
            raise

        self.trans = trans

    def __repr__(self) -> str:
        return "Trans(np.ndarray)"

    def __str__(self) -> str:
        return f"{self.trans}"

    def __getitem__(self, key):
        return self.trans[key]

    def __setitem__(self, key, value):
        self.trans[key] = value

    def __eq__(self, o: object) -> bool:
        if np.all(self.trans == o.trans):
            return True
        return False

    @property
    def coord(self):
        return self.trans[:3, 3]

    @coord.setter
    def coord(self, transl):
        if isinstance(transl, list):
            transl = np.array(transl)
        self.trans[:3, 3] = transl

    @property
    def rot(self):
        return self.trans[:3, :3]

    @rot.setter
    def rot(self, rot: np.ndarray):
        try:
            if rot.ndim != 2 or rot.shape[0] != 3 or rot.shape[1] != 3:
                raise RuntimeError("rotation matrice must 3x3")
        except RuntimeError as e:
            print(repr(e))
            raise
        self.trans[:3, :3] = rot

    @property
    def euler(self):
        et = Euler_trans
        gamma, beta, alpha = et.trans2zyx(self.trans)
        return np.array([gamma, beta, alpha])


class Robot:
    def __init__(
        self,
        dh_array: np.ndarray,
        name: Optional[str] = None,
        dh_angle: Type_angle = Type_angle.RAD,
        dh_type: Type_DH = Type_DH.STANDARD,
        is_revol_list: Optional[List[bool]] = None,
    ) -> None:

        self.dh_array = dh_array
        self.name = name
        self.links_count = dh_array.shape[0]
        self.dh_type = dh_type
        self.is_revol_list = is_revol_list
        if is_revol_list is None:
            self.is_revol_list = [True] * self.links_count

        try:
            if self.dh_type != Type_DH.STANDARD and self.dh_type != Type_DH.MODIFIED:
                raise RuntimeError("Please assign attributes in 'Type_DH'")
            if dh_angle == Type_angle.RAD:
                pass
            elif dh_angle == Type_angle.DEG:
                self.dh_array[:, 0] = np.radians(self.dh_array[:, 0])
                self.dh_array[:, 3] = np.radians(self.dh_array[:, 3])
            else:
                raise RuntimeError("Please assign attributes in 'Type_angle'")
            if len(self.is_revol_list) != self.links_count:
                raise RuntimeError(
                    f"Length of is_revol_list should be {self.links_count}, \
                        but now is {len(self.is_revol_list)}"
                )
        except RuntimeError as e:
            print(repr(e))
            raise

    @property
    def is_pieper(self) -> bool:
        joints_ang = [0] * self.links_count
        trans = self.forword_kine(joints_ang, save_links=True)
        if self.links_count != 6:
            return "Irrelevat to Pieper-Criterion"
        if np.all(trans[-3].coord == trans[-1].coord):
            return True
        return False

    def forword_kine(
        self, joints_ang: Optional[Union[List, np.ndarray]] = None, save_links: bool = False
    ) -> Union[Trans, List[Trans]]:
        dh_array = self.dh_array
        if joints_ang is None:
            joints_ang = [0] * self.links_count

        if dh_array.ndim == 1:
            dh_array = dh_array[None, :]

        if isinstance(joints_ang, list):
            joints_ang = np.array(joints_ang)
        try:
            if joints_ang.ndim > 1:
                raise RuntimeError("Assign 1D List or np.ndarray to 'joints_ang'")
            if len(joints_ang) != self.links_count:
                raise RuntimeError(
                    f"Number of joints should be {self.links_count}, but now is {len(joints_ang)}"
                )
        except RuntimeError as e:
            print(repr(e))
            raise

        trans = Trans(np.eye(4))
        links_trans = []
        for i in range(self.links_count):
            is_revol = self.is_revol_list[i]
            if is_revol:
                theta = dh_array[i, 0] + joints_ang[i]
                d = dh_array[i, 1]
            else:
                theta = dh_array[i, 0]
                d = dh_array[i, 1] + joints_ang[i]
            a = dh_array[i, 2]
            alpha = dh_array[i, 3]
            mat_theta = Coord_trans.mat_rotz(theta)
            mat_d = Coord_trans.mat_transl([0, 0, d])
            mat_a = Coord_trans.mat_transl([a, 0, 0])
            mat_alpha = Coord_trans.mat_rotx(alpha)

            trans = copy.deepcopy(trans)
            if self.dh_type == Type_DH.MODIFIED:
                trans.trans = trans.trans.dot(mat_alpha).dot(mat_a).dot(mat_d).dot(mat_theta)
            else:
                trans.trans = trans.trans.dot(mat_theta).dot(mat_d).dot(mat_a).dot(mat_alpha)
            if save_links:
                links_trans.append(trans)
        if save_links:
            return links_trans
        return trans

    # todo: if is_pieper is False
    def inverse_kine_simplex(
        self, coord: Union[List, np.ndarray], init_ang: Union[List, np.ndarray], euler=None, save_err=False
    ) -> np.ndarray:
        def fitness(joints):
            trans = self.forword_kine(joints, save_links=False)
            coord_fit = trans.coord
            err = np.sqrt(np.sum(np.square(coord - coord_fit)))
            return err

        if isinstance(coord, list):
            coord = np.array(coord)
        if isinstance(init_ang, list):
            init_ang = np.array(init_ang)

        try:
            if coord.ndim > 1:
                raise RuntimeError("Assign 1D List or np.ndarray to 'coord'")
            if init_ang.ndim > 1:
                raise RuntimeError("Assign 1D List or np.ndarray to 'init_ang'")
            if len(init_ang) != self.links_count:
                raise RuntimeError(
                    f"Number of joints should be {self.links_count}, but now is {len(init_ang)}"
                )
            if len(coord) != 3:
                raise RuntimeError("Length of 'coord' should be 3")
        except RuntimeError as e:
            print(repr(e))
            raise

        if self.is_pieper or isinstance(self.is_pieper, str):
            res = simplex(
                fitness, init_ang, 1e-2, 10e-6, 300, 2000, 1, 2, 1 / 2, 1 / 2, log_opt=True, print_opt=False
            )
        else:
            try:
                if euler is None:
                    raise RuntimeError("Please assign euler angles")
            except RuntimeError as e:
                print(repr(e))
                raise

        joints = res[0]
        err = res[1]

        try:
            if err >= 0.1:
                raise Warning("Error is greater than 0.1")
        except Warning as e:
            print(repr(e))

        if save_err:
            return joints, err

        return joints


class Plot:
    @staticmethod
    def plot_robot(trans_list: List[Trans], save_path: Optional[str] = None) -> None:
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        p_x = []
        p_y = []
        p_z = []
        for t in trans_list:
            p_x.append(np.round(t.coord[0], 4))
            p_y.append(np.round(t.coord[1], 4))
            p_z.append(np.round(t.coord[2], 4))
        ax.plot3D(p_x, p_y, p_z, "-r")
        ax.plot3D(p_x, p_y, p_z, ".b")
        if save_path:
            plt.savefig(save_path)
        plt.show()
        plt.close()
        plt.cla()
        plt.clf()
