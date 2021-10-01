from RobotCK import *
import numpy as np

dh_puma = np.genfromtxt('./DHForm/puma.csv', delimiter=',')
puma = Robot(dh_puma, 'puma', dh_angle='deg')
puma_ik_1 = puma.inverse_kine_simplex([500, 240, 230], [0., 0., 0., 0., 0., 0.])
puma_ik_2 = puma.inverse_kine_simplex([500, 240, 230], [0.1, -1, -2, 0., 0., 0.])
puma_fk_1 = puma.forword_kine(puma_ik_1, save_links=True)
puma_fk_2 = puma.forword_kine(puma_ik_2, save_links=True)
print(puma_ik_1)
print(puma_ik_2)
# print(puma_fk_1.coord)
# print(puma_fk_2.coord)

dh_er4ia = np.genfromtxt('./DHForm/er4ia.csv', delimiter=',')
er4ia = Robot(dh_er4ia, 'er4ia', dh_angle='deg')

test = Trans(np.eye(4))
test2 = np.arange(6).reshape((2, 3))
test3 = test[:] + test[:]
test4 = [1, 2, 3]
test[0, 1:4] = np.array([3, 3, 4])
print(test)
