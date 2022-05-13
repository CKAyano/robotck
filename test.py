from RobotCK import Euler_trans, Robot, Type_DH, Type_angle, Plot, Coord_trans
import numpy as np
from itertools import product
import sympy as sp


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


def table_2() -> None:
    d1 = 800
    d4 = 1000
    d5 = 15
    d6 = 200
    a2 = 1150
    a3 = 250
    a5 = 100
    dh = np.array(
        [[0, d1, 0, 0], [0, 0, a2, 0], [0, 0, a3, np.pi / 2], [0, d4, 0, 0], [0, d5, a5, 0], [0, d6, 0, 0]]
    )
    robot = Robot(dh, dh_angle=Type_angle.RAD, dh_type=Type_DH.STANDARD)
    fkine = robot.forword_kine([0.5, 0.5, 0, 0, 0, 0], save_links=True)

    point = fkine[-1].coord
    print(point)
    Plot.plot_robot(fkine)


def fanuc():
    th1, th2, th3, th4, th5, th6 = sp.symbols("th1 th2 th3 th4 th5 th6")
    d1, d2, d3, d4, d5, d6 = sp.symbols("d1 d2 d3 d4 d5 d6")
    a1, a2, a3, a4, a5, a6 = sp.symbols("a1 a2 a3 a4 a5 a6")
    # ap1, ap2, ap3, ap4, ap5, ap6 = sp.symbols("ap1 ap2 ap3 ap4 ap5 ap6")
    # dh = sp.Matrix(
    #     [
    #         [th1, 0, 0, -sp.pi / 2],
    #         [th2 - sp.pi / 2, 0, 260, 0],
    #         [th3, 0, 20, -sp.pi / 2],
    #         [th4, 290, 0, sp.pi / 2],
    #         [th5, 0, 0, -sp.pi / 2],
    #         [th6, 0, 0, 0],
    #     ]
    # )
    dh = sp.Matrix(
        [
            [th1, d1, a1, 0],
            [th2, d2, a2, 0],
            [th3, d3, a3, sp.pi / 2],
            [th4, d4, 0, sp.pi / 2],
            [th5, 0, 0, -sp.pi / 2],
            [th6, 0, 0, 0],
        ]
    )
    table1 = Robot(dh, "table1", dh_angle=Type_angle.SYM, dh_type=Type_DH.STANDARD)
    test = table1._inverse_kine_sym_th1_3([th1, th2, th3], "23")
    for t in test:
        print(t)
        print()


def test():
    joints_range = [[[-90, 0], [0, 90]], [[-110, -40], [-40, 30]]]

    for pro in product("01", repeat=2):
        pro = list(map(int, pro))

        for i, rg in enumerate(pro):
            range_joint = joints_range[i][rg]
            rand_angle = "rand的code, 得出第i軸第rg組隨機角度"

        save_data = "存第一組model的資料"


def euler_angle_test():
    dh_er4ia = np.genfromtxt("./DHForm/er4ia.csv", delimiter=",")
    er4ia = Robot(dh_er4ia, "er4ia", dh_angle=Type_angle.DEG)
    t = er4ia.forword_kine([0, 0, 0, 0, np.pi / 2, 0])
    # ea = np.radians([20, 30, 0])
    # print(ea)
    # t = Euler_trans.xyz2trans(ea[2], ea[1], ea[0])
    # t = Euler_trans.zyx2trans(ea[0], ea[1], ea[2])
    e = Euler_trans.trans2zyx(t)
    # print(t)
    print(t.euler)
    print(t.rot)


if __name__ == "__main__":
    euler_angle_test()
