import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Optional
from robotck.links import Links
from robotck.homomatrix import HomoMatrix
from robotck.dh_types import DHType
import robotck.math as MathCK
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform


def _arrow3D(ax, x, y, z, dx, dy, dz, *args, **kwargs):
    '''Add an 3d arrow to an `Axes3D` instance.'''

    arrow = Arrow3D(x, y, z, dx, dy, dz, *args, **kwargs)
    ax.add_artist(arrow)


setattr(Axes3D, 'arrow3D', _arrow3D)


class Arrow3D(FancyArrowPatch):

    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = (x, y, z)
        self._dxdydz = (dx, dy, dz)

    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)

    def do_3d_projection(self, renderer=None):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))

        return np.min(zs)


def _coordinate_arrow(start: List, end: List, ax: Axes3D, color: str):
    ax.arrow3D(
        start[0], start[1], start[2], end[0], end[1], end[2],
        mutation_scale=20,
        ec='black',
        fc=color)


def _plot_arrow(ax, t: HomoMatrix, arrow_start, arrow_end_org, color: str):
    arrow_end_x = MathCK.matmul(
        t.matrix, MathCK.matrix(
            [[arrow_end_org[0]],
                [arrow_end_org[1]],
                [arrow_end_org[2]],
                [1]]
        )
    )
    _coordinate_arrow(
        arrow_start,
        [
            float(arrow_end_x[0]) - arrow_start[0],
            float(arrow_end_x[1]) - arrow_start[1],
            float(arrow_end_x[2]) - arrow_start[2]
        ],
        ax,
        color
    )


def _data_for_cylinder_along_z(center_x, center_y, radius, height_z):
    z = np.linspace(0, height_z, 10)
    theta = np.linspace(0, 2 * np.pi, 10)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * np.cos(theta_grid) + center_x
    y_grid = radius * np.sin(theta_grid) + center_y
    return x_grid, y_grid, z_grid


def _set_axes_equal(ax):
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


def plot_robot(
    trans_list: Links,
    dh_type,
    joints_radius=10.0,
    show_coord: bool = True,
    save_path: Optional[str] = None
) -> None:
    fig = plt.figure()
    ax = Axes3D(fig)

    height_z = joints_radius * 5
    arrow_length = height_z * 1.5

    cx, cy, cz = _data_for_cylinder_along_z(0, 0, joints_radius, height_z)
    cz = cz - height_z / 2
    x_t = np.zeros(cx.shape)
    y_t = np.zeros(cy.shape)
    z_t = np.zeros(cz.shape)

    if dh_type == DHType.STANDARD:
        p_x = [0]
        p_y = [0]
        p_z = [0]
        ax.plot_surface(cx, cy, cz, rstride=1, cstride=1, linewidth=0, alpha=1)
    else:
        p_x = []
        p_y = []
        p_z = []

    for i, t in enumerate(trans_list):
        t: HomoMatrix
        p_x.append(np.round(t.coord[0], 4))
        p_y.append(np.round(t.coord[1], 4))
        p_z.append(np.round(t.coord[2], 4))

        if show_coord:
            arrow_start = t.get_coord_list()
            _plot_arrow(ax, t, arrow_start, [arrow_length, 0, 0], "red")
            _plot_arrow(ax, t, arrow_start, [0, arrow_length, 0], "green")
            _plot_arrow(ax, t, arrow_start, [0, 0, arrow_length], "blue")

        if i == len(trans_list) - 1:
            if dh_type == DHType.STANDARD:
                break

        for n, (x, y, z) in enumerate(zip(cx, cy, cz)):
            for i in range(x.size):
                temp = MathCK.matmul(t.matrix, MathCK.matrix([[x[i]], [y[i]], [z[i]], [1]]))
                x_t[n, i] = float(temp[0])
                y_t[n, i] = float(temp[1])
                z_t[n, i] = float(temp[2])

        ax.plot_surface(x_t, y_t, z_t, rstride=1, cstride=1, linewidth=0, alpha=1)

    ax.plot3D(p_x, p_y, p_z, "-r")
    ax.plot3D(p_x, p_y, p_z, ".b")
    _set_axes_equal(ax)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    if save_path:
        plt.savefig(save_path)
    plt.show()
    plt.close()
    plt.cla()
    plt.clf()
