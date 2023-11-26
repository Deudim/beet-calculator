import numpy as np
import utils


a = np.arange(15, 21, 0.3)
b = np.arange(0.05, 1, 0.05)
b_matrix = []
for i in range(20):
    cache = np.arange(0.05, 1, 0.05)
    np.random.shuffle(cache)
    b_matrix.append(cache)

b_matrix = np.array(b_matrix)

np.random.shuffle(a)

P = np.zeros((20, 20))

for i in range(20):
    P[i][0] = a[i]
    product = a[i]
    for j in range(1, 20):
        product *= b_matrix[i][j - 1]
        P[i][j] = product


p_list = P.tolist()

print(utils.hungarian(p_list, 'max'))
