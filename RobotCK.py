from argparse import ArgumentError
from tkinter import Variable
from typing import List, Optional, Union
from xml.dom.minidom import Attr
import numpy as np
import copy
import Package.NelderMeadSimplex as simplex
from enum import Enum, auto
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sympy as sp


def deg2rad(matrix):
    return matrix * np.pi / 180


def rad2deg(matrix):
    return matrix * 180 / np.pi


class DHForm:
    def __init__(self) -> None:
        pass

    def standard():
        pass

    def modified():
        pass


class DHAngleType(Enum):
    RAD = auto()
    DEG = auto()
    SYM = auto()


class DHType(Enum):
    STANDARD = auto()
    MODIFIED = auto()


class MathCK:
    __type = np

    def set_type(type):
        try:
            if type != np and type != sp:
                raise ArgumentError("type should be np.matrix or sp.Matrix")
        except ArgumentError as e:
            print(repr(e))
            raise
        MathCK.__type = type

    def pi():
        return MathCK.__type.pi

    def matrix(array):
        if MathCK.__type == np:
            return MathCK.__type.matrix(array)
        if MathCK.__type == sp:
            return MathCK.__type.Matrix(array)

    def cos(angle):
        return MathCK.__type.cos(angle)

    def sin(angle):
        return MathCK.__type.sin(angle)

    def sqrt(num):
        return MathCK.__type.sqrt(num)

    def atan2(num1, num2):
        if MathCK.__type == np:
            return MathCK.__type.arctan2(num1, num2)
        if MathCK.__type == sp:
            return MathCK.__type.atan2(num1, num2)


class Coord_trans:
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


class EulerAngle:
    def trans2zyx(trans) -> List:
        if MathCK.sqrt(trans[0, 0] ** 2 + trans[1, 0] ** 2) == 0 and -trans[2, 0] == 1:
            b = MathCK.pi / 2
            a = 0
            r = MathCK.atan2(trans[0, 1], trans[1, 1])
        elif MathCK.sqrt(trans[0, 0] ** 2 + trans[1, 0] ** 2) == 0 and -trans[2, 0] == -1:
            b = -MathCK.pi / 2
            a = 0
            r = -MathCK.atan2(trans[0, 1], trans[1, 1])
        else:
            b = MathCK.atan2(-trans[2, 0], MathCK.sqrt(trans[0, 0] ** 2 + trans[1, 0] ** 2))
            cb = MathCK.cos(b)
            a = MathCK.atan2(trans[1, 0] / cb, trans[0, 0] / cb)
            r = MathCK.atan2(trans[2, 1] / cb, trans[2, 2] / cb)
        return [a, b, r]

    # ! not finish todo
    def zyx2trans(alpha, beta, gamma) -> Union[np.matrix, sp.Matrix]:
        ct = Coord_trans
        return ct.mat_rotz(alpha) * ct.mat_roty(beta) * ct.mat_rotx(gamma)

    # ! not finish todo
    def xyz2trans(gamma, beta, alpha) -> Union[np.matrix, sp.Matrix]:
        ct = Coord_trans
        return ct.mat_rotx(gamma) * ct.mat_roty(beta) * ct.mat_rotz(alpha)


class FixedAngle:
    pass


class HomoMatrix:
    def __init__(self, matrix: Union[np.ndarray, np.matrix, sp.Matrix]) -> None:
        try:
            is_ndarray = isinstance(matrix, np.ndarray)
            is_ndmatrix = isinstance(matrix, np.matrix)
            is_spmatrix = isinstance(matrix, sp.Matrix)
            if is_ndarray or is_ndmatrix or is_spmatrix:
                pass
            else:
                raise ArgumentError("input type is wrong")
        except ArgumentError as e:
            print(repr(e))
            raise

        self._error_raising(matrix)

        if isinstance(matrix, np.ndarray):
            matrix = np.asmatrix(matrix)

        self.matrix = matrix
        self.axis_matrix = None

    def _error_raising(self, trans):
        try:
            if trans.shape[0] != 4 or trans.shape[1] != 4:
                raise RuntimeError("Transfer matrice must 3x3")
        except RuntimeError as e:
            print(repr(e))
            raise

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
        try:
            if not isinstance(transl, self.matrix):
                raise ArgumentError("input type is wrong")
        except ArgumentError as e:
            print(repr(e))
            raise
        self.matrix[:3, 3] = transl

    @property
    def rot(self):
        return self.matrix[:3, :3]

    @rot.setter
    def rot(self, rot):
        try:
            if not isinstance(rot, self.matrix):
                raise ArgumentError("input type is wrong")
        except ArgumentError as e:
            print(repr(e))
            raise

        try:
            if rot.shape[0] != 3 or rot.shape[1] != 3:
                raise RuntimeError("rotation matrice must 3x3")
        except RuntimeError as e:
            print(repr(e))
            raise

        self.matrix[:3, :3] = rot

    @property
    def zyxeuler(self):
        return EulerAngle.trans2zyx(self.matrix)

    @property
    def xyzfixed(self):
        return EulerAngle.trans2zyx(self.matrix)


class Robot:
    def __init__(
        self,
        dh_array: np.ndarray,
        name: Optional[str] = None,
        dh_angle: DHAngleType = DHAngleType.RAD,
        dh_type: DHType = DHType.STANDARD,
        is_revol_list: Optional[List[bool]] = None,
    ) -> None:

        self.dh_array = dh_array
        self._set_matrix_type()
        self.name = name
        self.links_count = dh_array.shape[0]
        self.dh_type = dh_type
        self.is_revol_list = is_revol_list
        if is_revol_list is None:
            self.is_revol_list = [True] * self.links_count

        try:
            if self.dh_type != DHType.STANDARD and self.dh_type != DHType.MODIFIED:
                raise RuntimeError("Please assign attributes in 'Type_DH'")
            if dh_angle == DHAngleType.RAD:
                pass
            elif dh_angle == DHAngleType.DEG:
                self.dh_array[:, 0] = deg2rad(self.dh_array[:, 0])
                self.dh_array[:, 3] = deg2rad(self.dh_array[:, 3])
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

    def _set_matrix_type(self):
        if isinstance(self.dh_array, sp.Matrix):
            MathCK.set_type(sp)
        else:
            MathCK.set_type(np)

    def forword_kine(
        self, joints_ang: Optional[Union[List, np.ndarray]] = None, save_links: bool = False
    ) -> Union[HomoMatrix, List[HomoMatrix]]:
        dh_array = self.dh_array
        if joints_ang is None:
            joints_ang = [0] * self.links_count

        # if dh_array.ndim == 1:
        #     dh_array = dh_array[None, :]

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

        matrix_eye = MathCK.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        homomat = HomoMatrix(matrix_eye)
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

            homomat = copy.deepcopy(homomat)
            if self.dh_type == DHType.MODIFIED:
                axis_matrix = mat_alpha * mat_a * mat_d * mat_theta
                homomat.matrix = homomat.matrix * axis_matrix
            else:
                axis_matrix = mat_theta * mat_d * mat_a * mat_alpha
                homomat.matrix = homomat.matrix * axis_matrix
            if save_links:
                homomat.axis_matrix = axis_matrix
                links_trans.append(homomat)
        if save_links:
            return links_trans
        return homomat

    def inverse_kine_pieper(self, coordinate: List):
        # todo
        try:
            if len(coordinate) != 3:
                raise ArgumentError("length of argument should be 3")
        except ArgumentError as e:
            print(repr(e))
            raise

        try:
            if self.dh_type == DHType.STANDARD:
                if self.dh_array[0, 2] != 0:
                    raise RuntimeError("This DH could not solve by pieper, because a1 is not 0")
        except RuntimeError as e:
            print(repr(e))
            raise

        round_count = 6

        x, y, z = coordinate
        MathCK.set_type(sp)
        th1, th2, th3, th4, th5, th6 = sp.symbols("th1 th2 th3 th4 th5 th6")

        homomat = self.forword_kine([th1, th2, th3, th4, th5, th6], save_links=True)
        ExpressionHandle._round_homoMatirx(homomat, round_count)
        ExpressionHandle._convert_homomatrix_float_to_pi(homomat)

        f = homomat[2].axis_matrix * homomat[3].axis_matrix[:, -1]
        f = ExpressionHandle._round_expr(f, round_count)
        f = ExpressionHandle._convert_float_to_pi(f)

        g = homomat[1].axis_matrix * f
        # g = sp.simplify(g)
        g = ExpressionHandle._round_expr(g, round_count)
        g = ExpressionHandle._convert_float_to_pi(g)

        # r = g[0, 0] ** 2 + g[1, 0] ** 2 + g[2, 0] ** 2 - x ** 2 - y ** 2 - z ** 2
        r = g[0] ** 2 + g[1] ** 2 + g[2] ** 2 - x ** 2 - y ** 2 - z ** 2
        r = sp.simplify(r)
        r = ExpressionHandle._round_expr(r, round_count)
        r = ExpressionHandle._convert_float_to_pi(r)

        eq = homomat[0].axis_matrix * g - MathCK.matrix([[x], [y], [z], [1]])
        # eq = sp.simplify(eq)
        eq = ExpressionHandle._round_expr(eq, round_count)
        eq = ExpressionHandle._convert_float_to_pi(eq)
        eq_1 = eq[0]
        eq_2 = eq[1]
        eq_3 = eq[2]

        angle_temp = np.zeros((0, 3))
        q3s = ExpressionHandle._solve(r, th3)
        q3s = self._angleAdj(q3s)
        # q3s = self._unique(q3s, 8)

        for q3 in q3s:
            eq_3_copy = eq_3.copy()
            eq_3_copy = eq_3_copy.subs(th3, sp.Float(q3))
            q2s = ExpressionHandle._solve(eq_3_copy, th2)
            for q2 in q2s:
                ang = np.array([[0, float(q2), float(q3)]])
                angle_temp = np.vstack((angle_temp, ang))
        for i in range(angle_temp.shape[0]):
            angle_temp[i, :] = self._angleAdj(angle_temp[i, :])

        joint_angle = np.zeros((0, 3))
        for ang in angle_temp:
            eq_1_copy = eq_1.copy()
            ang_q2 = ang[1]
            ang_q3 = ang[2]
            eq_1_copy = eq_1_copy.subs(th2, sp.Float(ang_q2))
            eq_1_copy = eq_1_copy.subs(th3, sp.Float(ang_q3))
            # q1s = sp.solve(eq_1_copy, th1)
            q1s = ExpressionHandle._solve(eq_1_copy, th1)
            for q1 in q1s:
                ang_add_q1 = ang.copy()
                ang_add_q1[0] = float(q1)
                joint_angle = np.vstack((joint_angle, ang_add_q1))

        for i in range(joint_angle.shape[0]):
            joint_angle[i, :] = self._angleAdj(joint_angle[i, :])

        joint_angle = self._unique(joint_angle, 8)

        keep_index = []
        for i, ang in enumerate(joint_angle):
            eq_2_c = eq_2.copy()
            eq_2_c = eq_2_c.subs([(th1, ang[0]), (th2, ang[1]), (th3, ang[2])])
            if abs(float(eq_2_c) - 0) <= 0.0001:
                keep_index.append(i)

        joint_angle = joint_angle[keep_index, :]

        if not isinstance(self.dh_array, sp.Matrix):
            MathCK.set_type(np)

        return joint_angle

    @staticmethod
    def _angleAdj(ax):
        # lim_list = [1000, 100, 10, 1]
        for ii in range(len(ax)):
            # for lim in lim_list:
            while ax[ii] > np.pi:
                ax[ii] = ax[ii] - np.pi * 2

            while ax[ii] < -np.pi:
                ax[ii] = ax[ii] + np.pi * 2
        return ax

    @staticmethod
    def _unique(joint_angle, thr):
        need_convert = False
        if isinstance(joint_angle, list):
            need_convert = True
        _, q3s_idx = np.unique(np.round(joint_angle, thr), axis=0, return_index=True)
        joint_angle = joint_angle[q3s_idx]
        if need_convert:
            joint_angle = joint_angle.tolist()
        return joint_angle

    def _inverse_kine_sym_th1_3(self, theta_sym, num_theta):
        trans = self._forword_kine_sym(save_links=True)
        x, y, z = sp.symbols("x y z")
        f = trans[2].axis_t * trans[3].axis_t[:, -1]
        g = trans[1].axis_t * f
        r = g[0, 0] ** 2 + g[1, 0] ** 2 + g[2, 0] ** 2 - x ** 2 - y ** 2 - z ** 2
        r = sp.simplify(r)
        eq = trans[0].axis_t * g - sp.Matrix([[x], [y], [z], [1]])
        eq = sp.simplify(eq)

        output = []
        if num_theta == 3:
            t3 = sp.solve(r, theta_sym[2])
            for t in t3:
                output.append(sp.simplify(t))
        if num_theta == 2:
            eq2 = eq[2, :]
            t2 = sp.solve(eq2, theta_sym[1])
            for t in t2:
                output.append(sp.simplify(t))
        if num_theta == 1:
            eq3 = eq[0, :]
            t1 = sp.solve(eq3, theta_sym[0])
            for t in t1:
                output.append(sp.simplify(t))
        if num_theta == "23":
            eq23_1 = eq[0, :]
            eq23_2 = eq[1, :]
            tt = sp.solve([eq23_1, eq23_2], [theta_sym[0], theta_sym[1]])
            for t in tt:
                output.append(sp.simplify(t))
        return output

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

    def plot(self, angle_rad):
        pass


class Plot:
    # PRE_TRANS =
    def getCynByAxis(redius=1, heightStart=0, heightEnd=5, offset=[0, 0, 0], devision=20, mainAxis="z"):

        mainAxis = mainAxis.lower()

        theta = np.linspace(0, 2 * np.pi, devision)
        cx = np.array([redius * np.cos(theta)])
        cz = np.array([heightStart, heightEnd])
        cx, cz = np.meshgrid(cx, cz)
        cy = np.array([redius * np.sin(theta)] * 2)

        if mainAxis == "z":
            return offset[0] + cx, offset[1] + cy, offset[2] + cz
        elif mainAxis == "y":
            return offset[0] + cx, offset[1] + cz, offset[2] + cy
        elif mainAxis == "x":
            return offset[0] + cz, offset[1] + cy, offset[2] + cx
        else:
            raise ValueError("'x', 'y' or 'z' PLZ")

    def drawCylinder(ax, px, py, pz):

        cx, cy, cz = Plot.getCynByAxis(
            offset=[px, py, pz], devision=40, mainAxis="x", heightEnd=5, heightStart=0, redius=10
        )

        # fig = plt.figure(figsize=(11, 10))
        # ax = plt.axes(projection="3d")
        ax.plot_surface(cx, cy, cz, rstride=1, cstride=1, linewidth=0, alpha=0.25)
        # ax.set_xlim(-5, 5)
        # ax.set_ylim(-5, 5)
        # ax.set_zlim(0, 10)
        # plt.show()

    def set_axes_equal(ax):
        x_limits = ax.get_xlim3d()
        y_limits = ax.get_ylim3d()
        z_limits = ax.get_zlim3d()

        x_range = abs(x_limits[1] - x_limits[0])
        x_middle = np.mean(x_limits)
        y_range = abs(y_limits[1] - y_limits[0])
        y_middle = np.mean(y_limits)
        z_range = abs(z_limits[1] - z_limits[0])
        z_middle = np.mean(z_limits)

        plot_radius = 0.5 * max([x_range, y_range, z_range])

        ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
        ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
        ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

    def plot_robot(trans_list: List[HomoMatrix], save_path: Optional[str] = None) -> None:
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        p_x = [0]
        p_y = [0]
        p_z = [0]
        for t in trans_list:
            p_x.append(np.round(t.coord[0], 4))
            p_y.append(np.round(t.coord[1], 4))
            p_z.append(np.round(t.coord[2], 4))
        ax.plot3D(p_x, p_y, p_z, "-r")
        # for x, y, z in zip(p_x, p_y, p_z):
        #     Plot.drawCylinder(ax, x, y, z)
        ax.plot3D(p_x, p_y, p_z, ".b")
        Plot.set_axes_equal(ax)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        if save_path:
            plt.savefig(save_path)
        plt.show()
        plt.close()
        plt.cla()
        plt.clf()


class ExpressionHandle:
    def _round_expr(expr, n):
        expr_c = expr
        for a in sp.preorder_traversal(expr):
            if isinstance(a, sp.Float):
                expr_c = expr_c.subs(a, round(a, n))
        return expr_c

    def _round_homoMatirx(homoMatrix: Union[List[HomoMatrix], HomoMatrix], n):
        if isinstance(homoMatrix, HomoMatrix):
            m = [HomoMatrix]
        for m in homoMatrix:
            m.matrix = ExpressionHandle._round_expr(m.matrix, n)
            m.axis_matrix = ExpressionHandle._round_expr(m.axis_matrix, n)

    def _convert_float_to_pi(expr):
        expr_c = expr
        n = 5
        pi_round_n = round(np.pi, n)
        for a in sp.preorder_traversal(expr):
            if isinstance(a, sp.Float):
                rounded_a = round(float(a), n)
                if abs(rounded_a - pi_round_n) < 0.00001:
                    expr_c = expr_c.subs(a, sp.pi)
                if abs(rounded_a + pi_round_n) < 0.00001:
                    expr_c = expr_c.subs(a, -sp.pi)
                if abs(rounded_a - pi_round_n / 2) < 0.00001:
                    expr_c = expr_c.subs(a, sp.pi / 2)
                if abs(rounded_a + pi_round_n / 2) < 0.00001:
                    expr_c = expr_c.subs(a, -sp.pi / 2)
        return expr_c

    def _convert_homomatrix_float_to_pi(homoMatrix: Union[List[HomoMatrix], HomoMatrix]):
        if isinstance(homoMatrix, HomoMatrix):
            m = [HomoMatrix]
        for m in homoMatrix:
            m.matrix = ExpressionHandle._convert_float_to_pi(m.matrix)
            m.axis_matrix = ExpressionHandle._convert_float_to_pi(m.axis_matrix)

    def _solve(expr, symbol):
        solver = ExpressionHandle._nsolve_pass_when_error
        start_list = [0, np.pi / 2, np.pi, 3 * np.pi / 2]
        output = []
        for start in start_list:
            q = solver(expr, symbol, start)
            if q:
                output.append(q)
        return output

    def _nsolve_pass_when_error(expr, symbol, start):
        try:
            q = sp.nsolve(expr, symbol, start)
            return q
        except Exception:
            pass
