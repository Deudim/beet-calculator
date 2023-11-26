import numpy as np
import utils




# a = np.arange(15, 21, 0.3)
# #b = np.arange(0.05, 1, 0.05)
# K = np.arange(5, 7.5, 0.13)
# Na = np.arange(0.3, 0.9, 0.031)
# N = np.arange(1.5, 3, 0.076)
# np.random.shuffle(K)
# np.random.shuffle(Na)
# np.random.shuffle(N)
#
# B = 0.12 * (K + Na) + 0.24 * N + 0.48
#
# print(B)
#
# b_matrix = []
# for i in range(20):
#     cache = np.arange(0.05, 1, 0.05)
#     np.random.shuffle(cache)
#     b_matrix.append(cache)
#
# b_matrix = np.array(b_matrix)
#
# np.random.shuffle(a)
#
# Z = np.zeros((20, 20))
#
# for i in range(20):
#     Z[i][0] = a[i] - B[i]
#     product = a[i]
#     for j in range(1, 20):
#         product *= b_matrix[i][j - 1]
#         product -= B[i]
#         Z[i][j] = product
#
# print(Z)
# z_list = Z.tolist()

s_opt = []
s_greedy = []
for i in range(10000):
    z_m = utils.create_matrix_z()
    s_opt.append(utils.hungarian(z_m, 'max')['result'])
    s_greedy.append(utils.greedy(z_m, 'max')['result'])

opt = np.array(s_opt)
opt = opt.mean()
greedy = np.array(s_greedy)
greedy = greedy.mean()

print(f'greedy error is {abs(opt - greedy)}')


