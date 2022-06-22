import numpy as np
import scipy as sp
from typing import Optional, List, Union
from dh_types import DHAngleType, DHType
from transformation import Coord_trans, EulerAngle, _MathCK
from homomatrix import HomoMatrix
from plot import Plot
from nelder_mead_simplex import simplex
import copy


def deg2rad(matrix):
    return matrix * np.pi / 180


def rad2deg(matrix):
    return matrix * 180 / np.pi


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
            _MathCK.set_type(sp)
        else:
            _MathCK.set_type(np)

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

        matrix_eye = _MathCK.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
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
        if len(coordinate) != 3:
            raise TypeError("length of argument should be 3")

        if self.dh_type == DHType.STANDARD:
            if self.dh_array[0, 2] != 0:
                raise RuntimeError("This DH could not solve by pieper, because a1 is not 0")

        round_count = 6

        x, y, z = coordinate
        _MathCK.set_type(sp)
        th1, th2, th3, th4, th5, th6 = sp.symbols("th1 th2 th3 th4 th5 th6")

        homomat = self.forword_kine([th1, th2, th3, th4, th5, th6], save_links=True)
        _ExpressionHandle._round_homoMatirx(homomat, round_count)
        _ExpressionHandle._convert_homomatrix_float_to_pi(homomat)

        f = homomat[2].axis_matrix * homomat[3].axis_matrix[:, -1]
        f = _ExpressionHandle._round_expr(f, round_count)
        f = _ExpressionHandle._convert_float_to_pi(f)

        g = homomat[1].axis_matrix * f
        # g = sp.simplify(g)
        g = _ExpressionHandle._round_expr(g, round_count)
        g = _ExpressionHandle._convert_float_to_pi(g)

        # r = g[0, 0] ** 2 + g[1, 0] ** 2 + g[2, 0] ** 2 - x ** 2 - y ** 2 - z ** 2
        r = g[0] ** 2 + g[1] ** 2 + g[2] ** 2 - x ** 2 - y ** 2 - z ** 2
        r = sp.simplify(r)
        r = _ExpressionHandle._round_expr(r, round_count)
        r = _ExpressionHandle._convert_float_to_pi(r)

        eq = homomat[0].axis_matrix * g - _MathCK.matrix([[x], [y], [z], [1]])
        # eq = sp.simplify(eq)
        eq = _ExpressionHandle._round_expr(eq, round_count)
        eq = _ExpressionHandle._convert_float_to_pi(eq)
        eq_1 = eq[0]
        eq_2 = eq[1]
        eq_3 = eq[2]

        angle_temp = np.zeros((0, 3))
        q3s = _ExpressionHandle._solve(r, th3)
        q3s = self._angleAdj(q3s)
        # q3s = self._unique(q3s, 8)

        for q3 in q3s:
            eq_3_copy = eq_3.copy()
            eq_3_copy = eq_3_copy.subs(th3, sp.Float(q3))
            q2s = _ExpressionHandle._solve(eq_3_copy, th2)
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
            q1s = _ExpressionHandle._solve(eq_1_copy, th1)
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
            _MathCK.set_type(np)

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
        t = self.forword_kine(angle_rad, save_links=True)
        Plot.plot_robot(t, self.dh_type)


class _ExpressionHandle:
    @staticmethod
    def _round_expr(expr, n):
        expr_c = expr
        for a in sp.preorder_traversal(expr):
            if isinstance(a, sp.Float):
                expr_c = expr_c.subs(a, round(a, n))
        return expr_c

    @staticmethod
    def _round_homoMatirx(homoMatrix: Union[List[HomoMatrix], HomoMatrix], n):
        if isinstance(homoMatrix, HomoMatrix):
            m = [HomoMatrix]
        for m in homoMatrix:
            m.matrix = _ExpressionHandle._round_expr(m.matrix, n)
            m.axis_matrix = _ExpressionHandle._round_expr(m.axis_matrix, n)

    @staticmethod
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

    @staticmethod
    def _convert_homomatrix_float_to_pi(homoMatrix: Union[List[HomoMatrix], HomoMatrix]):
        if isinstance(homoMatrix, HomoMatrix):
            m = [HomoMatrix]
        for m in homoMatrix:
            m.matrix = _ExpressionHandle._convert_float_to_pi(m.matrix)
            m.axis_matrix = _ExpressionHandle._convert_float_to_pi(m.axis_matrix)

    @staticmethod
    def _solve(expr, symbol):
        solver = _ExpressionHandle._nsolve_pass_when_error
        start_list = [0, np.pi / 2, np.pi, 3 * np.pi / 2]
        output = []
        for start in start_list:
            q = solver(expr, symbol, start)
            if q:
                output.append(q)
        return output

    @staticmethod
    def _nsolve_pass_when_error(expr, symbol, start):
        try:
            q = sp.nsolve(expr, symbol, start)
            return q
        except Exception:
            pass
