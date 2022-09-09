from robotck import Robot
from robotck import DHAngleType, DHType
import numpy as np
import sympy as sp


def puma_std():
    ang_90 = np.pi / 2

    dh = {
        "theta": [0, 0, 0, 0, 0, 0],
        "d": [0, 149.09, 0, 433.07, 0, 0],
        "a": [0, 431.8, -20.32, 0, 0, 0],
        "alpha": [-ang_90, 0, ang_90, -ang_90, ang_90, 0],
    }

    # 生成機械手臂物件（需代入DH參數）
    puma = Robot(dh, "puma", dh_angle=DHAngleType.RAD, dh_type=DHType.STANDARD)
    puma.plot([0, 0, 2.8, 0, 0, 0])


def puma_mod():
    ang_90 = np.pi / 2

    dh = {
        "alpha": [0, -ang_90, 0, -ang_90, ang_90, -ang_90],
        "a": [0, 0, 431.8, 20.32, 0, 0],
        "d": [0, 0, 149.09, 433.07, 0, 0],
        "theta": [0, 0, 0, 0, 0, 0],
    }

    # 生成機械手臂物件（需代入DH參數）
    puma = Robot(dh, "puma", dh_angle=DHAngleType.RAD, dh_type=DHType.MODIFIED)

    # 計算順向運動解
    ang = np.radians([20, -30, 30, 0, 0, 0])
    # ang = np.radians([0, 0, 0, 0, 0, 0])
    fkine = puma.forword_kine(ang)
    fkine.round(4)
    print(f"第1軸旋轉矩陣: \n{fkine[0].rot}")
    print(f"第3軸座標: \n{fkine[2].coord}")
    print(f"第5軸齊次座標: \n{fkine[4].matrix}")
    print(f"最後一軸座標: \n{fkine[-1].coord}")
    print(f"等同於: \n{fkine.end_effector.coord}")
    print(f"最後一軸齊次也可直接print: \n{fkine}")

    print(f"最後一軸zyx歐拉角: \n{fkine[-1].zyxeuler}\n")

    print(f"也可以用'get_joint'方法(取第2軸): \n{fkine.get_joint(2)}")

    # puma._validate_ik(fkine[-1])

    # 使用pieper方法計算前三軸逆向運動解
    ikine = puma.inverse_kine_pieper_first_three([320, 280, -200])
    print(f"共4組逆向運動解: \n{ikine}\n")

    # 畫機械手臂姿態
    puma.plot(ang, joint_radius=20)


def puma_symbol():
    ang_90 = np.pi / 2
    dh = {
        "alpha": [0, -ang_90, 0, -ang_90, ang_90, -ang_90],
        "a": [0, 0, "a2", "a3", 0, 0],
        "d": [0, 0, "d3", "d4", 0, 0],
        "theta": [0, 0, 0, 0, 0, 0],
    }

    puma = Robot(dh, "puma", dh_angle=DHAngleType.RAD, dh_type=DHType.MODIFIED)

    ang = ["th1", "th2", "th3", "th4", "th5", "th6"]
    fkine = puma.forword_kine(ang)
    fkine.round(4)
    print(f"第1軸旋轉矩陣: \n{fkine[0].rot}")
    print(f"第3軸座標: \n{fkine[2].coord}")
    print(f"第5軸齊次座標: \n{sp.simplify(fkine[4].matrix)}")
    print(f"最後一軸座標: \n{sp.simplify(fkine[-1].coord)}")
    print(f"最後一軸zyx歐拉角: \n{sp.simplify(fkine[-1].zyxeuler)}\n")

    ikine = puma.inverse_kine_pieper_first_three([320, 280, -200])
    print(f"前三軸共4組逆向運動解: \n{ikine}\n")


if __name__ == "__main__":
    puma_mod()
