import numpy as np
import copy
from Package.NelderMeadSimplex import simplex


class Coord_trans:

    @staticmethod
    def mat_rotx(alpha):
        mat = np.array([
            [1, 0, 0, 0],
            [0, np.cos(alpha), -np.sin(alpha), 0],
            [0, np.sin(alpha), np.cos(alpha), 0],
            [0, 0, 0, 1]])
        return mat

    @staticmethod
    def mat_roty(beta):
        mat = np.array([
            [np.cos(beta), 0, np.sin(beta), 0],
            [0, 1, 0, 0],
            [-np.sin(beta), 0, np.cos(beta), 0],
            [0, 0, 0, 1]])
        return mat

    @staticmethod
    def mat_rotz(theta):
        mat = np.array([
            [np.cos(theta), -np.sin(theta), 0, 0],
            [np.sin(theta), np.cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])
        return mat

    @staticmethod
    def mat_transl(transl_list: list):
        mat = np.array([
            [1, 0, 0, transl_list[0]],
            [0, 1, 0, transl_list[1]],
            [0, 0, 1, transl_list[2]],
            [0, 0, 0, 1]])
        return mat


class Euler_trans:

    @staticmethod
    def trans2Euler(trans):
        if np.sqrt(trans[0, 0]**2 + trans[1, 0]**2) == 0 and -trans[2, 0] == 1:
            b = np.pi/2
            a = 0
            r = np.arctan2(trans[0, 1], trans[1, 1])
        elif np.sqrt(trans[0, 0]**2 + trans[1, 0]**2) == 0 and -trans[2, 0] == -1:
            b = -np.pi/2
            a = 0
            r = -np.arctan2(trans[0, 1], trans[1, 1])
        else:
            b = np.arctan2(-trans[2, 0], np.sqrt(trans[0, 0]**2 + trans[1, 0]**2))
            cb = np.cos(b)
            a = np.arctan2(trans[1, 0]/cb, trans[0, 0]/cb)
            r = np.arctan2(trans[2, 1]/cb, trans[2, 2]/cb)
        return [r, b, a]

    @staticmethod
    def euler2Trans(gamma, beta, alpha):
        ct = Coord_trans
        return ct.mat_rotz(alpha).dot(ct.mat_roty(beta).dot(ct.mat_rotx(gamma)))


class Trans:

    def __init__(self, trans: np.ndarray) -> None:
        try:
            if trans.ndim != 2 or trans.shape[0] != 4 or trans.shape[1] != 4:
                raise RuntimeError('Transfer matrice must 3x3')
        except RuntimeError as e:
            print(repr(e))
            raise

        self.trans = trans

    def __repr__(self) -> str:
        return 'Trans(np.ndarray)'

    def __str__(self) -> str:
        return f'{self.trans}'

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
                raise RuntimeError('rotation matrice must 3x3')
        except RuntimeError as e:
            print(repr(e))
            raise
        self.trans[:3, :3] = rot

    @property
    def euler(self):
        et = Euler_trans
        gamma, beta, alpha = et.trans2Euler(self.trans)
        return np.array([gamma, beta, alpha])

    # @euler.setter
    # def euler(self, gamma, beta, alpha):
    #     et = Euler_trans
    #     self.trans = et.euler2Trans(gamma, beta, alpha)


class Robot:

    def __init__(self, dh_array, name=None,
                 dh_angle='rad', dh_type='standard', is_revol_list=None) -> None:
        self.dh_array = dh_array
        self.name = name
        self.count_links = dh_array.shape[0]
        self.dh_type = dh_type
        self.is_revol_list = is_revol_list
        if is_revol_list is None:
            self.is_revol_list = [True] * self.count_links

        try:
            if self.dh_type != 'standard' and self.dh_type != 'modified':
                raise RuntimeError("There's only 'standard' and 'modified' for mode")
            if dh_angle == 'rad':
                pass
            elif dh_angle == 'deg':
                self.dh_array[:, 0] = np.radians(self.dh_array[:, 0])
                self.dh_array[:, 3] = np.radians(self.dh_array[:, 3])
            else:
                raise RuntimeError("There's only 'rad' or 'deg' for dh_angle")
            if len(self.is_revol_list) != self.count_links:
                raise RuntimeError(
                    f"Length of is_revol_list should be {self.count_links}, \
                        but now is {len(self.is_revol_list)}")
        except RuntimeError as e:
            print(repr(e))
            raise

    @property
    def is_pieper(self):
        joints_ang = [0] * self.count_links
        trans = self.forword_kine(joints_ang, save_links=True)
        if self.count_links < 6:
            return 'Irrelevat to Pieper-Criterion'
        if np.all(trans[-3].coord == trans[-1].coord):
            return True
        return False

    def forword_kine(self, joints_ang=None, save_links=False):
        dh_array = self.dh_array
        if joints_ang is None:
            joints_ang = [0] * self.count_links

        if dh_array.ndim == 1:
            dh_array = dh_array[None, :]
        try:
            if len(joints_ang) != self.count_links:
                raise RuntimeError(
                    f"Number of joints should be {self.count_links}, but now is {len(joints_ang)}")
        except RuntimeError as e:
            print(repr(e))
            raise

        trans = Trans(np.eye(4))
        links_trans = []
        for i in range(self.count_links):
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
            if self.dh_type == 'modified':
                trans.trans = trans.trans.dot(mat_alpha).dot(mat_a).dot(mat_d).dot(mat_theta)
            else:
                trans.trans = trans.trans.dot(mat_theta).dot(mat_d).dot(mat_a).dot(mat_alpha)
            if save_links:
                links_trans.append(trans)
        if save_links:
            return links_trans
        return trans

    # todo: if is_pieper is False
    def inverse_kine_simplex(self, coord, init_ang: list,
                             euler=None, save_err=False):
        def fitness(joints):
            trans = self.forword_kine(joints, save_links=False)
            coord_fit = trans.coord
            err = np.sqrt(np.sum(np.square(coord-coord_fit)))
            return err

        if isinstance(coord, list):
            coord = np.array(coord)
        if isinstance(init_ang, list):
            init_ang = np.array(init_ang)

        try:
            if len(init_ang) != self.count_links:
                raise RuntimeError(
                    f"Number of joints should be {self.count_links}, but now is {len(init_ang)}")
        except RuntimeError as e:
            print(repr(e))
            raise

        if self.is_pieper or isinstance(self.is_pieper, str):
            res = simplex(fitness, init_ang, 1e-2, 10e-6, 300, 2000,
                          1, 2, 1/2, 1/2, log_opt=True, print_opt=False)
        else:
            try:
                if euler is None:
                    raise RuntimeError('Please assign euler angles')
            except RuntimeError as e:
                print(repr(e))
                raise

        joints = res[0]
        err = res[1]

        try:
            if err >= 0.1:
                raise Warning('Error is greater than 0.1')
        except Warning as e:
            print(repr(e))

        if save_err:
            return joints, err

        return joints
