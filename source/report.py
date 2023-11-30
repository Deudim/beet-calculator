from mat_backend import hungarian, munkres, greedy, create_matrix_z
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import os


def make_report():
    df = pd.DataFrame(columns=['Венгерский', 'Жадный', 'Разница', 'итерация'])
    future_mean_hung = [[] for j in range(20)]
    future_mean_greed = [[] for i in range(20)]

    for step in range(50):
        z = create_matrix_z()
        hung = hungarian(z, 'max')
        res_hung_on_i = 0
        greed = greedy(z, 'max')
        res_greed_on_i = 0

        for i in range(len(hung['rows'])):
            res_hung_on_i += z[hung['rows'][i]][hung['cols'][i]]/100
            future_mean_hung[i].append(res_hung_on_i)

            res_greed_on_i += z[greed['rows'][i]][greed['cols'][i]]/100
            future_mean_greed[i].append(res_greed_on_i)

            difference = abs(res_hung_on_i - res_greed_on_i)
            df.loc[len(df)] = [res_hung_on_i, res_greed_on_i, difference, step]

    hung_mean_numpy = np.zeros(20)
    greed_mean_numpy = np.zeros(20)

    for i in range(20):
        hung_mean_numpy[i] = np.mean(future_mean_hung[i])
        greed_mean_numpy[i] = np.mean(future_mean_greed[i])

    days = np.arange(1, 21, 1)

    plt.plot(days, hung_mean_numpy, label='Венгерсикй')
    plt.plot(days, greed_mean_numpy, label='Жадный')
    plt.xlabel('Дни')
    plt.ylabel('Кг сахара')
    plt.legend()
    #plt.show()

    os.mkdir('out')
    plt.savefig('out/my_plot.png')
    df.to_csv('out/report.csv', index=False)


