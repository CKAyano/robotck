from robotck import Robot
from robotck import DHAngleType, DHType
import numpy as np
import sympy as sp


def puma():
    ang_90 = np.pi / 2

    # 生成DH參數

    # 方法 1
    # dh = np.matrix(
    #     [
    #         [0, 0, 0, 0],
    #         [0, 0, 0, -ang_90],
    #         [0, 149.09, 431.8, 0],
    #         [0, 433.07, 20.32, -ang_90],
    #         [0, 0, 0, ang_90],
    #         [0, 0, 0, -ang_90],
    #     ]
    # )

    # 方法 2（推薦）
    dh = {
        "theta": [0, 0, 0, 0, 0, 0],
        "d": [0, 0, 149.09, 433.07, 0, 0],
        "a": [0, 0, 431.8, 20.32, 0, 0],
        "alpha": [0, -ang_90, 0, -ang_90, ang_90, -ang_90],
    }

    # 生成機械手臂物件（需代入DH參數）
    puma = Robot(dh, "puma", dh_angle=DHAngleType.RAD, dh_type=DHType.MODIFIED)

    # 計算順向運動解
    ang = np.radians([20, -30, 30, 0, 0, 0])
    fkine = puma.forword_kine(ang, save_links=True)
    print(f"第1軸旋轉矩陣: \n{fkine[0].rot}")
    print(f"第3軸座標: \n{fkine[2].coord}")
    print(f"第5軸齊次座標: \n{fkine[4].matrix}")
    print(f"最後一軸座標: \n{fkine[-1].coord}")
    print(f"最後一軸zyx歐拉角: \n{fkine[-1].zyxeuler}\n")

    # 使用pieper方法計算前三軸逆向運動解
    ikine = puma.inverse_kine_pieper_first_three([320, 280, -200])
    print(f"共4組逆向運動解: \n{ikine}\n")

    # 畫機械手臂姿態
    puma.plot(ang, joint_radius=20)