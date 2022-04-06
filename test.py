from RobotCK import *
import numpy as np


def main_1() -> None:
    dh_er4ia = np.genfromtxt("./DHForm/er4ia.csv", delimiter=",")
    er4ia = Robot(dh_er4ia, "er4ia", dh_angle=Type_angle.DEG)
    q2 = 20

    ang = np.radians(np.array([0, 0, 0, 0, -90, 0]))
    t = er4ia.forword_kine(ang, save_links=True)
    # eu = Euler_trans.zyx2trans(0.3, 0.2, 0.1)
    # eu_2 = Euler_trans.xyz2trans(0.1, 0.2, 0.3)
    # tt = Euler_trans.trans2zyx(eu)
    # tt_2 = Euler_trans.trans2zyx(eu_2)
    # print(eu)
    # print(eu_2)
    # print(tt)
    # print(tt_2)
    Plot.plot_robot(t)


def main_2() -> None:
    dh_custom = np.genfromtxt("./DHForm/custom.csv", delimiter=",")
    custom = Robot(dh_custom, "custom", Type_angle.DEG, Type_DH.MODIFIED)
    ang = np.radians(np.array([50, -20, 30]))
    # transf = custom.forword_kine([0, 0, 0], True)
    transf = custom.forword_kine(ang, True)
    for t in transf:
        c = np.round(t.coord, 4)
        print(c)
    Plot.plot_robot(transf)


def main_3() -> None:
    points_range = [[1, 11], [1, 7], [0, 0]]
    toe_in_angle = np.arctan2(sum(points_range[1]), sum(points_range[0]))
    point = [4, 5, 0]
    t_01 = Coord_trans.mat_rotz(toe_in_angle)
    t_02 = Coord_trans.mat_transl(point).dot(Coord_trans.mat_rotz(toe_in_angle))
    # print(t - t_0)
    t_12 = np.linalg.inv(t_01).dot(t_02)
    print(t_12)


if __name__ == "__main__":
    # main_2()
    main_1()
