import numpy as np
import sympy as sp
from typing import Optional, List, Tuple, TypeVar, Union
from .dh_types import DHAngleType, DHType
from .transformation import Coord_trans
from .math import MathCK
from .homomatrix import HomoMatrix
from .links import Links
from .expressionHandler import ExpressionHandler
from .plot import Plot
from .nelder_mead_simplex import simplex
import copy


T = TypeVar('T', HomoMatrix, Links)


class DHParameterError(Exception):
    pass


def deg2rad(matrix):
    return matrix * np.pi / 180


def rad2deg(matrix):
    return matrix * 180 / np.pi


def angleAdj(ax):
    for ii in range(len(ax)):
        # for lim in lim_list:
        while ax[ii] > np.pi:
            ax[ii] = ax[ii] - np.pi * 2

        while ax[ii] < -np.pi:
            ax[ii] = ax[ii] + np.pi * 2
    return ax


def unique(joint_angle, thr):
    need_convert = False
    if isinstance(joint_angle, list):
        need_convert = True
    _, q3s_idx = np.unique(np.round(joint_angle, thr), axis=0, return_index=True)
    joint_angle = joint_angle[q3s_idx]
    if need_convert:
        joint_angle = joint_angle.tolist()
    return joint_angle


def dh_dict_to_ndarray(dh_param: dict):
    theta_array = _dh_key_to_2darray(dh_param, "theta")
    d_array = _dh_key_to_2darray(dh_param, "d")
    a_array = _dh_key_to_2darray(dh_param, "a")
    alpha_array = _dh_key_to_2darray(dh_param, "alpha")
    try:
        dh_array = MathCK.hstack((theta_array, d_array, a_array, alpha_array))
        return dh_array
    except sp.matrices.common.ShapeError as e:
        print(repr(e))
        raise DHParameterError("dh parameter length should be the same")
    except ValueError as e:
        print(repr(e))
        raise DHParameterError("dh parameter length should be the same")


def _dh_key_to_2darray(dh_param, key: str):
    dh_value = dh_param[key]
    if not isinstance(dh_value, list):
        raise TypeError("type of value of dh_param should be List")
    if MathCK.is_type("sympy"):
        dh_value = _convert_str_to_symbols(dh_value)
        mat = MathCK.matrix(dh_value)
        return mat.T.T

    mat = MathCK.matrix(dh_value)
    return mat[:, None]


def _convert_str_to_symbols(dh_value_list):
    for i, v in enumerate(dh_value_list):
        if isinstance(v, str):
            v_s = sp.symbols(v)
            dh_value_list[i] = v_s
    return dh_value_list


def set_matrix_type(dh_param):
    if isinstance(dh_param, dict):
        _set_matrix_type_by_dh_dict(dh_param)
        return

    if isinstance(dh_param, sp.Matrix):
        MathCK.set_type("sympy")
    else:
        MathCK.set_type("numpy")


def _set_matrix_type_by_dh_dict(dh_dict: dict):
    for v in dh_dict.values():
        if any(isinstance(i, str) for i in v):
            MathCK.set_type("sympy")
            return
    MathCK.set_type("numpy")
    return


class Robot:
    def __init__(
        self,
        dh_param: dict | np.ndarray | sp.Matrix,
        name: Optional[str] = None,
        dh_angle: DHAngleType = DHAngleType.RAD,
        dh_type: DHType = DHType.STANDARD,
        is_revol_list: Optional[List[bool]] = None,
    ) -> None:

        set_matrix_type(dh_param)

        if isinstance(dh_param, dict):
            self.dh_array = dh_dict_to_ndarray(dh_param)
        else:
            self.dh_array = dh_param

        self.name = name
        self.links_count = self.dh_array.shape[0]
        self.dh_type = dh_type

        self.is_revol_list: List[bool]
        if is_revol_list is None:
            self.is_revol_list = [True] * self.links_count
        else:
            self.is_revol_list = is_revol_list

        if self.dh_type != DHType.STANDARD and self.dh_type != DHType.MODIFIED:
            raise RuntimeError("Please assign attributes in 'DHType'")
        if dh_angle == DHAngleType.RAD:
            pass
        elif dh_angle == DHAngleType.DEG:
            self.dh_array[:, 0] = deg2rad(self.dh_array[:, 0])
            self.dh_array[:, 3] = deg2rad(self.dh_array[:, 3])
        else:
            raise RuntimeError("Please assign attributes in 'DHAngleType'")
        if len(self.is_revol_list) != self.links_count:
            raise RuntimeError(
                f"Length of is_revol_list should be {self.links_count}, \
                    but now is {len(self.is_revol_list)}"
            )

    def forword_kine(self, joints_angle: Optional[List | np.ndarray] = None) -> Links:

        dh_array = self.dh_array

        if isinstance(joints_angle, np.ndarray):
            j_ang: np.ndarray = joints_angle
        else:
            joints_ang_list: List

            if joints_angle is None:
                joints_ang_list = [0.0] * self.links_count
            else:
                joints_ang_list = joints_angle

            j_ang: np.ndarray = np.array(joints_ang_list)

        if any(isinstance(j, sp.Symbol) for j in j_ang):
            MathCK.set_type("sympy")
        if j_ang.ndim > 1:
            raise RuntimeError("Assign 1D List or np.ndarray to 'joints_ang'")
        if len(j_ang) != self.links_count:
            raise RuntimeError(f"Number of joints should be {self.links_count}, but now is {len(j_ang)}")

        matrix_eye = MathCK.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        homomat = HomoMatrix(matrix_eye)
        # links_trans = []
        links_trans = Links(self.dh_type)
        for i in range(self.links_count):
            is_revol = self.is_revol_list[i]
            if is_revol:
                theta = dh_array[i, 0] + j_ang[i]
                d = dh_array[i, 1]
            else:
                theta = dh_array[i, 0]
                d = dh_array[i, 1] + j_ang[i]
            a = dh_array[i, 2]
            alpha = dh_array[i, 3]
            mat_theta = Coord_trans.mat_rotz(theta)
            mat_d = Coord_trans.mat_transl([0, 0, d])
            mat_a = Coord_trans.mat_transl([a, 0, 0])
            mat_alpha = Coord_trans.mat_rotx(alpha)

            homomat = copy.deepcopy(homomat)
            if self.dh_type == DHType.MODIFIED:
                axis_matrix = MathCK.matmul(mat_alpha, mat_a, mat_d, mat_theta)
            else:
                axis_matrix = MathCK.matmul(mat_theta, mat_d, mat_a, mat_alpha)

            homomat.matrix = MathCK.matmul(homomat.matrix, axis_matrix)
            homomat.axis_matrix = axis_matrix
            links_trans.append(homomat)

        return links_trans

    def inverse_kine_pieper_first_three(self, coordinate: List):
        # todo
        if len(coordinate) != 3:
            raise TypeError("length of argument should be 3")

        if self.dh_type == DHType.STANDARD:
            if self.dh_array[0, 2] != 0:
                raise RuntimeError("This DH could not solve by pieper, because a1 is not 0")

        round_count = 6

        x, y, z = coordinate
        MathCK.set_type("sympy")
        th1, th2, th3, th4, th5, th6 = sp.symbols("th1 th2 th3 th4 th5 th6")

        homomat = self.forword_kine([th1, th2, th3, th4, th5, th6])
        # homomat = links.end_effector
        homomat.round(round_count)
        homomat.float_to_pi()

        # f = homomat[2].axis_matrix * homomat[3].axis_matrix[:, -1]
        f = MathCK.matmul(homomat[2].axis_matrix, homomat[3].axis_matrix[:, -1])
        f = ExpressionHandler._convert_float_to_pi(f)

        # g = homomat[1].axis_matrix * f
        g = MathCK.matmul(homomat[1].axis_matrix, f)
        g = ExpressionHandler._convert_float_to_pi(g)

        r = g[0] ** 2 + g[1] ** 2 + g[2] ** 2 - x ** 2 - y ** 2 - z ** 2
        r = sp.expand(r)
        r = ExpressionHandler._round_expr(r, round_count)
        r = ExpressionHandler._convert_float_to_pi(r)
        r = sp.simplify(r)

        # eq = homomat[0].axis_matrix * g - MathCK.matrix([[x], [y], [z], [1]])
        eq = MathCK.matmul(homomat[0].axis_matrix, g) - MathCK.matrix([[x], [y], [z], [1]])
        eq = ExpressionHandler._round_expr(eq, round_count)
        eq = ExpressionHandler._convert_float_to_pi(eq)
        eq_1 = eq[0]
        eq_2 = eq[1]
        eq_3 = eq[2]

        angle_temp = np.zeros((0, 3))
        q3s = ExpressionHandler._solve(r, th3)
        q3s = angleAdj(q3s)

        for q3 in q3s:
            eq_3_copy = eq_3.copy()
            eq_3_copy = eq_3_copy.subs(th3, sp.Float(q3))
            q2s = ExpressionHandler._solve(eq_3_copy, th2)
            for q2 in q2s:
                ang = np.array([[0, float(q2), float(q3)]])
                angle_temp = np.vstack((angle_temp, ang))
        for i in range(angle_temp.shape[0]):
            angle_temp[i, :] = angleAdj(angle_temp[i, :])

        joint_angle = np.zeros((0, 3))
        for ang in angle_temp:
            eq_1_copy = eq_1.copy()
            ang_q2 = ang[1]
            ang_q3 = ang[2]
            eq_1_copy = eq_1_copy.subs(th2, sp.Float(ang_q2))
            eq_1_copy = eq_1_copy.subs(th3, sp.Float(ang_q3))
            q1s = ExpressionHandler._solve(eq_1_copy, th1)
            for q1 in q1s:
                ang_add_q1 = ang.copy()
                ang_add_q1[0] = float(q1)
                joint_angle = np.vstack((joint_angle, ang_add_q1))

        for i in range(joint_angle.shape[0]):
            joint_angle[i, :] = angleAdj(joint_angle[i, :])

        joint_angle = unique(joint_angle, 8)

        keep_index = []
        for i, ang in enumerate(joint_angle):
            eq_2_c = eq_2.copy()
            eq_2_c = eq_2_c.subs([(th1, ang[0]), (th2, ang[1]), (th3, ang[2])])
            if abs(float(eq_2_c) - 0) <= 0.0001:
                keep_index.append(i)

        joint_angle = joint_angle[keep_index, :]

        if not isinstance(self.dh_array, sp.Matrix):
            MathCK.set_type("numpy")

        return joint_angle

    # todo: if is_pieper is False
    def inverse_kine_simplex(
        self, coord: List | np.ndarray, init_ang: List | np.ndarray, save_err=False
    ) -> np.ndarray | Tuple:
        def fitness(joints):
            links = self.forword_kine(joints)
            coord_fit = links[-1].coord
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

        res = simplex.simplex(
            fitness, init_ang, 1e-2, 10e-6, 300, 2000, 1, 2, 1 / 2, 1 / 2, log_opt=False, print_opt=False
        )

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

    def plot(self, angle_rad: Union[List, np.ndarray], joint_radius=10.0, save_path: Optional[str] = None):
        if MathCK.is_type("sympy"):
            raise TypeError("can not plot for dh with symbol")
        t = self.forword_kine(angle_rad)
        Plot.plot_robot(t, self.dh_type, joints_radius=joint_radius, save_path=save_path)

    def _validate_ik(self, homomatrix: HomoMatrix, err_thr=0.00001):
        coord_input = homomatrix.get_coord_list()
        iks = self.inverse_kine_pieper_first_three(coord_input)
        is_true_list = []
        for ik in iks:
            fk = self.forword_kine([ik[0], ik[1], ik[2], 0, 0, 0])
            print(fk[-1].get_coord_list())
            print(ik)
            if homomatrix.distance(fk) < err_thr:
                is_true_list.append(True)
                print(True)
            else:
                is_true_list.append(False)
                print(False)
            print()
        if all(is_true_list):
            print("ik is correct")
        else:
            print("ik is wrong")
