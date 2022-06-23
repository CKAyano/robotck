import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Optional
from .homomatrix import HomoMatrix
from .dh_types import DHType
from .math import MathCK


class Plot:
    @staticmethod
    def data_for_cylinder_along_z(center_x, center_y, radius, height_z):
        z = np.linspace(0, height_z, 10)
        theta = np.linspace(0, 2 * np.pi, 10)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = radius * np.cos(theta_grid) + center_x
        y_grid = radius * np.sin(theta_grid) + center_y
        return x_grid, y_grid, z_grid

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

    def plot_robot(trans_list: List[HomoMatrix], dh_type, save_path: Optional[str] = None) -> None:
        fig = plt.figure()
        ax = Axes3D(fig)

        height_z = 50
        cx, cy, cz = Plot.data_for_cylinder_along_z(0, 0, 10, height_z)
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
            p_x.append(np.round(t.coord[0, 0], 4))
            p_y.append(np.round(t.coord[1, 0], 4))
            p_z.append(np.round(t.coord[2, 0], 4))

            if i == len(trans_list) - 1:
                if dh_type == DHType.STANDARD:
                    break

            for n, (x, y, z) in enumerate(zip(cx, cy, cz)):
                for i in range(x.size):
                    temp = t.matrix * MathCK.matrix([[x[i]], [y[i]], [z[i]], [1]])
                    x_t[n, i] = float(temp[0])
                    y_t[n, i] = float(temp[1])
                    z_t[n, i] = float(temp[2])
            ax.plot_surface(x_t, y_t, z_t, rstride=1, cstride=1, linewidth=0, alpha=1)

        ax.plot3D(p_x, p_y, p_z, "-r")
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
