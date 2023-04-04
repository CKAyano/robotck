from enum import Enum, auto
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


class TrajectoryMethod(Enum):
    CUBIC = auto()
    QUINTIC = auto()
    PARABOLIC = auto()


def cubic_traj_s(a, b, c, d, t):
    traj_s_poly = np.poly1d([a, b, c, d])
    traj_s = traj_s_poly(t)
    t_s = np.hstack((t[:, None], traj_s[:, None]))
    return t_s


def cubic_traj_v(a, b, c, t):
    traj_v_poly = np.poly1d([3 * a, 2 * b, c])
    traj_v = traj_v_poly(t)
    t_v = np.hstack((t[:, None], traj_v[:, None]))
    return t_v


def cubic_traj_a(a, b, t):
    traj_a_poly = np.poly1d([6 * a, 2 * b])
    traj_a = traj_a_poly(t)
    t_a = np.hstack((t[:, None], traj_a[:, None]))
    return t_a


def quintic_traj_s(a, b, c, d, e, f, t):
    traj_s_poly = np.poly1d([a, b, c, d, e, f])
    traj_s = traj_s_poly(t)
    t_s = np.hstack((t[:, None], traj_s[:, None]))
    return t_s


def quintic_traj_v(a, b, c, d, e, t):
    traj_v_poly = np.poly1d([5 * a, 4 * b, 3 * c, 2 * d, e])
    traj_v = traj_v_poly(t)
    t_v = np.hstack((t[:, None], traj_v[:, None]))
    return t_v


def quintic_traj_a(a, b, c, d, t):
    traj_a_poly = np.poly1d([20 * a, 12 * b, 6 * c, 2 * d])
    traj_a = traj_a_poly(t)
    t_a = np.hstack((t[:, None], traj_a[:, None]))
    return t_a


def cubic_polynomial_formula(
    step_count: int,
    t_start: float,
    t_end: float,
    s_start: float,
    s_end: float,
    v_start=0.0,
    v_end=0.0,
    nargout=1,
):
    a = (
        -2 * s_end + 2 * s_start + t_end * v_end + t_end * v_start - t_start * v_end - t_start * v_start
    ) / (t_end**3 - 3 * t_end**2 * t_start + 3 * t_end * t_start**2 - t_start**3)
    b = (
        3 * s_end * t_end
        + 3 * s_end * t_start
        - 3 * s_start * t_end
        - 3 * s_start * t_start
        - t_end**2 * v_end
        - 2 * t_end**2 * v_start
        - t_end * t_start * v_end
        + t_end * t_start * v_start
        + 2 * t_start**2 * v_end
        + t_start**2 * v_start
    ) / (t_end**3 - 3 * t_end**2 * t_start + 3 * t_end * t_start**2 - t_start**3)
    c = (
        -6 * s_end * t_end * t_start
        + 6 * s_start * t_end * t_start
        + t_end**3 * v_start
        + 2 * t_end**2 * t_start * v_end
        + t_end**2 * t_start * v_start
        - t_end * t_start**2 * v_end
        - 2 * t_end * t_start**2 * v_start
        - t_start**3 * v_end
    ) / (t_end**3 - 3 * t_end**2 * t_start + 3 * t_end * t_start**2 - t_start**3)
    d = (
        3 * s_end * t_end * t_start**2
        - s_end * t_start**3
        + s_start * t_end**3
        - 3 * s_start * t_end**2 * t_start
        - t_end**3 * t_start * v_start
        - t_end**2 * t_start**2 * v_end
        + t_end**2 * t_start**2 * v_start
        + t_end * t_start**3 * v_end
    ) / (t_end**3 - 3 * t_end**2 * t_start + 3 * t_end * t_start**2 - t_start**3)

    time_step = np.linspace(t_start, t_end, step_count)
    if nargout == 1:
        s = cubic_traj_s(a, b, c, d, time_step)
        return s
    if nargout == 2:
        s = cubic_traj_s(a, b, c, d, time_step)
        v = cubic_traj_v(a, b, c, time_step)
        return s, v
    if nargout == 3:
        s = cubic_traj_s(a, b, c, d, time_step)
        v = cubic_traj_v(a, b, c, time_step)
        a = cubic_traj_a(a, b, time_step)
        return s, v, a
    if nargout not in [1, 2, 3]:
        raise TypeError("nargout should be 1 or 2 or 3")


def quintic_polynomial_matrix(
    step_count: int,
    t_start: float,
    t_end: float,
    s_start: float,
    s_end: float,
    v_start=0.0,
    v_end=0.0,
    a_start=0.0,
    a_end=0.0,
    nargout=1,
):
    poly_martix = np.array(
        [
            [t_start**5, t_start**4, t_start**3, t_start**2, t_start, 1],
            [t_end**5, t_end**4, t_end**3, t_end**2, t_end, 1],
            [5 * (t_start**4), 4 * (t_start**3), 3 * (t_start**2), 2 * t_start, 1, 0],
            [5 * (t_end**4), 4 * (t_end**3), 3 * (t_end**2), 2 * t_end, 1, 0],
            [20 * (t_start**3), 12 * (t_start**2), 6 * t_start, 2, 0, 0],
            [20 * (t_end**3), 12 * (t_end**2), 6 * t_end, 2, 0, 0],
        ]
    )
    traj_obj = np.array([s_start, s_end, v_start, v_end, a_start, a_end])
    traj_obj = traj_obj[:, None]
    poly_martix_inv = np.linalg.inv(poly_martix)
    coeffs = poly_martix_inv.dot(traj_obj)
    a, b, c, d, e, f = coeffs[0, 0], coeffs[1, 0], coeffs[2, 0], coeffs[3, 0], coeffs[4, 0], coeffs[5, 0]
    print(a, b, c, d, e, f)
    time_step = np.linspace(t_start, t_end, step_count)
    if nargout == 1:
        s = quintic_traj_s(a, b, c, d, e, f, time_step)
        return s
    if nargout == 2:
        s = quintic_traj_s(a, b, c, d, e, f, time_step)
        v = quintic_traj_v(a, b, c, d, e, time_step)
        return s, v
    if nargout == 3:
        s = quintic_traj_s(a, b, c, d, e, f, time_step)
        v = quintic_traj_v(a, b, c, d, e, time_step)
        a = quintic_traj_a(a, b, c, d, time_step)
        return s, v, a
    if nargout not in [1, 2, 3]:
        raise TypeError("nargout should be 1 or 2 or 3")


def quintic_polynomial_formula(
    step_count: int,
    t_start: float,
    t_end: float,
    s_start: float,
    s_end: float,
    v_start=0.0,
    v_end=0.0,
    a_start=0.0,
    a_end=0.0,
    nargout=1,
):

    a = (
        (6 / (t_start - t_end) ** 5) * (s_start - s_end)
        - (3 / (t_start + t_end) ** 4) * (v_start + v_end)
        + (1 / 2 * (t_start - t_end) ** 3) * (a_start - a_end)
    )

    b = (
        ((-15 * (t_start + t_end)) / (t_start - t_end) ** 5) * (s_start - s_end)
        + (1 / (t_start - t_end) ** 4)
        * ((7 * t_start + 8 * t_end) * v_start + (8 * t_start + 7 * t_end) * v_end)
        - (1 / (2 * (t_start - t_end) ** 3))
        * ((2 * t_start + 3 * t_end) * a_start - (3 * t_start + 2 * t_end) * a_end)
    )

    c = (
        ((10 * (t_start**2 + 4 * t_start * t_end + t_end**2)) / ((t_start - t_end) ** 5))
        * (s_start - s_end)
        - (2 / (t_start - t_end) ** 4)
        * (
            (2 * t_start**2 + 10 * t_start * t_end + 3 * t_end**2) * v_start
            + (3 * t_start**2 + 10 * t_start * t_end + 2 * t_end**2) * v_end
        )
        + (1 / 2 * (t_start - t_end) ** 3)
        * (
            (t_start**2 + 6 * t_start * t_end + 3 * t_end**2) * a_start
            - (3 * t_start**2 + 6 * t_start * t_end + t_end**2) * a_end
        )
    )

    d = (
        ((-30 * t_start * t_end * (t_start + t_end)) / ((t_start - t_end) ** 5)) * (s_start - s_end)
        + ((6 * t_start * t_end) / (t_start - t_end) ** 4)
        * ((2 * t_start + 3 * t_end) * v_start + (3 * t_start + 2 * t_end) * v_end)
        - (1 / 2 * (t_start - t_end) ** 3)
        * (
            t_end * (3 * t_start**2 + 6 * t_start * t_end + t_end**2) * a_start
            - t_start * (t_start**2 + 6 * t_start * t_end + 3 * t_end**2) * a_end
        )
    )

    e = (
        (30 * t_start**2 * t_end**2) / ((t_start - t_end) ** 5) * (s_start - s_end)
        + (1 / (t_start - t_end) ** 4)
        * (
            t_end**2 * (-6 * t_start + t_end) * (2 * t_start + t_end) * v_start
            - t_start**2 * (-t_start + 6 * t_end) * (t_start + 2 * t_end) * v_end
        )
        + ((t_start * t_end) / (2 * (t_start - t_end) ** 3))
        * ((t_end * (3 * t_start + 2 * t_end) * a_start) - (t_start * (2 * t_start + 3 * t_end) * a_end))
    )

    f = -(
        (1 / (t_start - t_end) ** 5)
        * (
            t_end**3 * (10 * t_start**2 - 5 * t_start * t_end + t_end**2) * s_start
            - t_start**3 * (t_start**2 - 5 * t_start * t_end + 10 * t_end**2) * s_end
        )
        + (t_start * t_end / (t_start - t_end) ** 4)
        * (t_end**2 * (4 * t_start - t_end) * v_start + t_start**2 * (-t_start + 4 * t_end) * v_end)
        - (t_start**2 * t_end**2) / (2 * (t_start - t_end) ** 3) * (t_end * a_start - t_start * a_end)
    )
    time_step = np.linspace(t_start, t_end, step_count)
    if nargout == 1:
        s = quintic_traj_s(a, b, c, d, e, f, time_step)
        return s
    if nargout == 2:
        s = quintic_traj_s(a, b, c, d, e, f, time_step)
        v = quintic_traj_v(a, b, c, d, e, time_step)
        return s, v
    if nargout == 3:
        s = quintic_traj_s(a, b, c, d, e, f, time_step)
        v = quintic_traj_v(a, b, c, d, e, time_step)
        a = quintic_traj_a(a, b, c, d, time_step)
        return s, v, a
    if nargout not in [1, 2, 3]:
        raise TypeError("nargout should be 1 or 2 or 3")


def plot_trajectory(*trajs, save_fig=False):
    plot_count = len(trajs)
    fig, axs = plt.subplots(plot_count, 1)
    fig.subplots_adjust(left=0.2, wspace=0.6)

    for i, p in enumerate(trajs):
        axs[i].plot(p[:, 0], p[:, 1])
        if i == 0:
            axs[i].set_xlabel("time")
            axs[i].set_ylabel("position (rad)")
        if i == 1:
            axs[i].set_xlabel("time")
            axs[i].set_ylabel("velocity (rad/s)")
        if i == 2:
            axs[i].set_xlabel("time")
            axs[i].set_ylabel("acceleration (rad/$s^2$)")
    fig.tight_layout()
    fig.align_ylabels(axs)
    if save_fig:
        plt.savefig("./fig.png", dpi=400)
    plt.show()


class Trajectory:
    def __init__(self, method) -> None:
        self.method = method
        if self.method == TrajectoryMethod.CUBIC:
            self.poly_function = cubic_polynomial_formula
        if self.method == TrajectoryMethod.QUINTIC:
            self.poly_function = quintic_polynomial_formula

    def get_trajectory(
        self,
        s_start: np.ndarray,
        s_stop: np.ndarray,
        t_start,
        t_end,
        step_period=1 / 20,
    ) -> Tuple[np.ndarray]:
        if s_start.ndim == 2:
            s_start = np.squeeze(s_start)
        if s_stop.ndim == 2:
            s_stop = np.squeeze(s_stop)

        dim_count = len(s_start)

        step_count = int((t_end - t_start) / step_period) + 1
        if step_count <= 2:
            return np.array([[t_start], [t_end]]), np.vstack((s_start, s_stop))

        s_out = np.empty((step_count, 0))
        for j in range(dim_count):
            s, v, a = self.poly_function(step_count, t_start, t_end, s_start[j], s_stop[j], nargout=3)
            s_out = np.hstack((s_out, s[:, 1:2]))
        # s_joints = np.hstack((s[:, 0:1], s_joints))
        return s[:, 0:1], s_out


if __name__ == "__main__":
    s_start, s_end, v_start, v_end, t_start, t_end = sp.symbols(
        "s_start, s_end, v_start, v_end, t_start, t_end"
    )
    poly_martix = sp.Matrix(
        [
            [t_start**3, t_start**2, t_start, 1],
            [t_end**3, t_end**2, t_end, 1],
            [3 * (t_start**2), 2 * t_start, 1, 0],
            [3 * (t_end**2), 2 * t_end, 1, 0],
        ]
    )
    traj_obj = sp.Matrix([s_start, s_end, v_start, v_end])
    poly_martix_inv = sp.simplify(poly_martix.inv())
    coeffs = poly_martix_inv * traj_obj
    sp.print_python(sp.simplify(sp.expand(coeffs)))
    print()
