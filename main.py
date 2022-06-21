from tkinter.tix import Tree
from RobotCK import EulerAngle, ExpressionHandle, Robot, DHType, DHAngleType, Plot, Coord_trans
import numpy as np
from itertools import product
import sympy as sp


def main_1() -> None:
    dh_er4ia = np.genfromtxt("./DHForm/er4ia.csv", delimiter=",")
    er4ia = Robot(dh_er4ia, "er4ia", dh_angle=DHAngleType.DEG)
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
    custom = Robot(dh_custom, "custom", DHAngleType.DEG, DHType.MODIFIED)
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
    robot = Robot(dh, dh_angle=DHAngleType.RAD, dh_type=DHType.STANDARD)
    fkine = robot.forword_kine([0.5, 0.5, 0, 0, 0, 0], save_links=True)

    point = fkine[-1].coord
    print(point)
    Plot.plot_robot(fkine)


def fanuc_sym():
    dh = sp.Matrix(
        [
            [0, 0, 0, -np.pi / 2],
            [0 - np.pi / 2, 0, 260, 0],
            [0, 0, 20, -np.pi / 2],
            [0, 290, 0, np.pi / 2],
            [0, 0, 0, -np.pi / 2],
            [0, 0, 0, 0],
        ]
    )

    fanuc = Robot(dh, "fanuc", dh_angle=DHAngleType.RAD, dh_type=DHType.STANDARD)

    th1, th2, th3, th4, th5, th6 = sp.symbols("th1 th2 th3 th4 th5 th6")

    p = fanuc.forword_kine([th1, th2, th3, th4, th5, th6], save_links=True)
    ExpressionHandle._round_homoMatirx(p, 4)
    for i in p:
        sp.pretty_print(sp.sympify(i.axis_matrix))
        sp.pretty_print(sp.sympify(i.matrix))
        print()


def fanuc():
    dh = np.matrix(
        [
            [0, 0, 0, -np.pi / 2],
            [0 - np.pi / 2, 0, 260, 0],
            [0, 0, 20, -np.pi / 2],
            [0, 290, 0, np.pi / 2],
            [0, 0, 0, -np.pi / 2],
            [0, 0, 0, 0],
        ]
    )

    fanuc = Robot(dh, "fanuc", dh_angle=DHAngleType.RAD, dh_type=DHType.STANDARD)

    # p = fanuc.forword_kine([0, 0, 0, 0, np.pi / 2, 0], save_links=True)
    ang = np.radians(np.array([20, 20, -30, 20, 70, 0]))
    fanuc.plot(ang)
    # print(np.round(p.zyxeuler, 4))
    # test = fanuc.inverse_kine_pieper([300, 20, 0])
    # for t in test:
    #     print(np.round(t, 6))

    # print()

    # # print(np.round(fanuc.forword_kine([0.0666, -0.4894, 2.79, 0, 0, 0]).coord, 4))

    # for ang in test:
    #     input = [ang[0], ang[1], ang[2], 0, 0, 0]
    #     t = fanuc.forword_kine(input)
    #     print(np.round(t.coord, 4))
    # for t in test:
    #     print(t)
    #     print()


def puma():
    dh = np.matrix(
        [
            [0, 0, 0, 0],
            [0, 0, 0, -np.pi / 2],
            [0, 149.09, 431.8, 0],
            [0, 433.07, 20.32, -np.pi / 2],
            [0, 0, 0, np.pi / 2],
            [0, 0, 0, -np.pi / 2],
        ]
    )
    puma = Robot(dh, "puma", dh_angle=DHAngleType.RAD, dh_type=DHType.MODIFIED)
    ang = np.radians([20, -30, 30, 0, 0, 0])
    sample = puma.forword_kine(ang, save_links=True)
    Plot.plot_robot(sample)
    sample = [float(i) for i in sample.coord]
    test = puma.inverse_kine_pieper(sample)
    for t in test:
        print(np.round(t, 6))

    print()

    # print(np.round(fanuc.forword_kine([0.0666, -0.4894, 2.79, 0, 0, 0]).coord, 4))

    for ang in test:
        input = [ang[0], ang[1], ang[2], 0, 0, 0]
        t = puma.forword_kine(input)
        print(np.round(t.coord, 4))
    # for t in test:
    #     print(t)
    #     print()


def fanuc_ik():
    th1, th2, th3, th4, th5, th6 = sp.symbols("th1 th2 th3 th4 th5 th6")
    d1, d2, d3, d4, d5, d6 = sp.symbols("d1 d2 d3 d4 d5 d6")
    a1, a2, a3, a4, a5, a6 = sp.symbols("a1 a2 a3 a4 a5 a6")
    # dh = sp.Matrix(
    #     [
    #         [0, 0, 0, 0],
    #         [0, 0, 0, -np.pi / 2],
    #         [0, 149.09, 431.8, 0],
    #         [0, 433.07, 20.32, -np.pi / 2],
    #         [0, 0, 0, np.pi / 2],
    #         [0, 0, 0, -np.pi / 2],
    #     ]
    # )
    dh = sp.Matrix(
        [
            [0, 0, 0, -sp.pi / 2],
            [0 - sp.pi / 2, 0, a2, 0],
            [0, 0, a3, -sp.pi / 2],
            [0, d4, 0, sp.pi / 2],
            [0, 0, 0, -sp.pi / 2],
            [0, 0, 0, 0],
        ]
    )
    fanuc = Robot(dh, "fanuc", dh_angle=DHAngleType.RAD, dh_type=DHType.STANDARD)
    # ang = np.radians([20, -30, 30, 0, 0, 0])
    sample = fanuc.forword_kine([th1, th2, th3, th4, th5, th6], save_links=True)
    ExpressionHandle._round_homoMatirx(sample, 4)
    a_35 = sample[3].axis_matrix * sample[4].axis_matrix * sample[5].axis_matrix
    a_35 = sp.simplify(a_35)
    r00, r01, r02, r10, r11, r12, r20, r21, r22 = sp.symbols("r00 r01 r02 r10 r11 r12 r20 r21 r22")
    t0, t1, t2 = sp.symbols("t0 t1 t2")
    e = sp.Matrix([[r00, r01, r02, t0], [r10, r11, r12, t1], [r20, r21, r22, t2], [0, 0, 0, 1]])
    lefty = sp.simplify(sample[2].matrix.inv() * e)

    for i, (a, b) in enumerate(zip(lefty.T, a_35.T)):
        print(f"{a} == {b}")
        if (i + 1) % 4 == 0:
            print()


def puma_ik():
    th1, th2, th3, th4, th5, th6 = sp.symbols("th1 th2 th3 th4 th5 th6")
    d1, d2, d3, d4, d5, d6 = sp.symbols("d1 d2 d3 d4 d5 d6")
    a1, a2, a3, a4, a5, a6 = sp.symbols("a1 a2 a3 a4 a5 a6")
    # dh = sp.Matrix(
    #     [
    #         [0, 0, 0, 0],
    #         [0, 0, 0, -np.pi / 2],
    #         [0, 149.09, 431.8, 0],
    #         [0, 433.07, 20.32, -np.pi / 2],
    #         [0, 0, 0, np.pi / 2],
    #         [0, 0, 0, -np.pi / 2],
    #     ]
    # )
    dh = sp.Matrix(
        [
            [0, 0, 0, 0],
            [0, 0, 0, -np.pi / 2],
            [0, d3, a2, 0],
            [0, d4, a3, -np.pi / 2],
            [0, 0, 0, np.pi / 2],
            [0, 0, 0, -np.pi / 2],
        ]
    )
    puma = Robot(dh, "puma", dh_angle=DHAngleType.RAD, dh_type=DHType.MODIFIED)
    # ang = np.radians([20, -30, 30, 0, 0, 0])
    sample = puma.forword_kine([th1, th2, th3, th4, th5, th6], save_links=True)
    ExpressionHandle._round_homoMatirx(sample, 4)
    a_35 = sample[3].axis_matrix * sample[4].axis_matrix * sample[5].axis_matrix
    a_35 = sp.simplify(a_35)
    r00, r01, r02, r10, r11, r12, r20, r21, r22 = sp.symbols("r00 r01 r02 r10 r11 r12 r20 r21 r22")
    t0, t1, t2 = sp.symbols("t0 t1 t2")
    e = sp.Matrix([[r00, r01, r02, t0], [r10, r11, r12, t1], [r20, r21, r22, t2], [0, 0, 0, 1]])
    lefty = sp.simplify(sample[2].matrix.inv() * e)

    for i, (a, b) in enumerate(zip(lefty.T, a_35.T)):
        print(f"{a} == {b}")
        if (i + 1) % 4 == 0:
            print()


def calc_puma_inv():
    th1, th2, th3, th4, th5, th6 = sp.symbols("th1 th2 th3 th4 th5 th6")
    r00, r01, r02, r10, r11, r12, r20, r21, r22 = sp.symbols("r00 r01 r02 r10 r11 r12 r20 r21 r22")
    t0, t1, t2 = sp.symbols("t0 t1 t2")
    q5 = (
        -1.0 * r02 * sp.sin(th2 + th3) * sp.cos(th1)
        - 1.0 * r12 * sp.sin(th1) * sp.sin(th2 + th3)
        - 1.0 * r22 * sp.cos(th2 + th3)
    )

    q6_u = (
        r01 * sp.sin(th2 + th3) * sp.cos(th1)
        + r11 * sp.sin(th1) * sp.sin(th2 + th3)
        + r21 * sp.cos(th2 + th3)
    )

    q6_d = (
        -r00 * sp.sin(th2 + th3) * sp.cos(th1)
        - r10 * sp.sin(th1) * sp.sin(th2 + th3)
        - r20 * sp.cos(th2 + th3)
    )

    q4_u = -r02 * sp.sin(th1) + r12 * sp.cos(th1)

    q4_d = (
        -r02 * sp.cos(th1) * sp.cos(th2 + th3)
        - r12 * sp.sin(th1) * sp.cos(th2 + th3)
        + r22 * sp.sin(th2 + th3)
    )

    # q5 = ExpressionHandle._solve(eq_1, th5)
    print(q5)


def symbol_example():
    # th1, th2, th3, th4, th5, th6 = sp.symbols("th1 th2 th3 th4 th5 th6")
    d1, d2, d3, d4, d5, d6 = sp.symbols("d1 d2 d3 d4 d5 d6")
    a1, a2, a3, a4, a5, a6 = sp.symbols("a1 a2 a3 a4 a5 a6")
    # ap1, ap2, ap3, ap4, ap5, ap6 = sp.symbols("ap1 ap2 ap3 ap4 ap5 ap6")
    dh = sp.Matrix(
        [
            [0, d1, a1, 0],
            [0, d2, a2, 0],
            [0, d3, a3, sp.pi / 2],
            [0, d4, 0, sp.pi / 2],
            [0, 0, 0, -sp.pi / 2],
            [0, 0, 0, 0],
        ]
    )
    table1 = Robot(dh, "table1", dh_angle=DHAngleType.RAD, dh_type=DHType.STANDARD)
    homoMatrix = table1.forword_kine([0, 0, 0, 0, 0, 0])
    print(homoMatrix)


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
    er4ia = Robot(dh_er4ia, "er4ia", dh_angle=DHAngleType.DEG)
    t = er4ia.forword_kine([0, 0, 0, 0, np.pi / 2, 0])
    # ea = np.radians([20, 30, 0])
    # print(ea)
    # t = Euler_trans.xyz2trans(ea[2], ea[1], ea[0])
    # t = Euler_trans.zyx2trans(ea[0], ea[1], ea[2])
    e = EulerAngle.trans2zyx(t)
    # print(t)
    print(t.zyxeuler)
    print(t.rot)


if __name__ == "__main__":
    # fanuc_sym()
    fanuc()
    # puma()
    # puma_sym()
    # fanuc_ik()
    # symbol_example()
