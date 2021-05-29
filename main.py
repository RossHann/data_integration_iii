# import numpy as np
# import similaritymeasures
# import matplotlib.pyplot as plt
#
# # Generate random experimental data
# x = np.random.random(100)
# y = np.random.random(100)
# exp_data = np.zeros((100, 2))
# exp_data[:, 0] = x
# exp_data[:, 1] = y
#
# # Generate random numerical data
# x = np.random.random(100)
# y = np.random.random(100)
# num_data = np.zeros((100, 2))
# num_data[:, 0] = x
# num_data[:, 1] = y
#
# print(num_data)
#
# # quantify the difference between the two curves using PCM
# # pcm = similaritymeasures.pcm(exp_data, num_data)
#
# # quantify the difference between the two curves using
# # Discrete Frechet distance
# # df = similaritymeasures.frechet_dist(exp_data, num_data)
#
# # quantify the difference between the two curves using
# # area between two curves
# # area = similaritymeasures.area_between_two_curves(exp_data, num_data)
#
# # quantify the difference between the two curves using
# # Curve Length based similarity measure
# # cl = similaritymeasures.curve_length_measure(exp_data, num_data)
#
# # quantify the difference between the two curves using
# # Dynamic Time Warping distance
# # dtw, d = similaritymeasures.dtw(exp_data, num_data)
#
# # print the results
# # print(pcm, df, area, cl, dtw)
# #
# # # plot the data
# # plt.figure()
# # plt.plot(exp_data[:, 0], exp_data[:, 1])
# # plt.plot(num_data[:, 0], num_data[:, 1])
# # plt.show()

# !/usr/bin/env python
from unicodedata import decimal

import similaritymeasures
from Similarity import *
import csv


def main():
    """ main function to create Similarity class instance and get use of it """

    measures = Similarity()

    csv_reader = csv.reader(open("./reformat/000002.csv", 'r', encoding='gbk'))
    n = 0
    data_set_1 = []
    for row in csv_reader:
        if n == 0:
            n += 1
            continue
        else:
            n += 1
            if row[4] == 'None':
                continue
            data_set_1.append(float(row[4]))

    csv_reader = csv.reader(open("./reformat/000004.csv", 'r', encoding='gbk'))
    n = 0
    data_set_2 = []
    for row in csv_reader:
        if n == 0:
            n += 1
            continue
        else:
            n += 1
            # print(row[4])
            if row[4] == 'None':
                continue
            data_set_2.append(float(row[4]))
    # print(data_set_2)
    print(measures.jaccard_similarity(data_set_1, data_set_2))

    # print(measures.euclidean_distance([0, 3, 4, 5], [7, 6, 3, -1]))
    # print(measures.jaccard_similarity([0, 1, 2, 5, 6], [0, 2, 3, 5, 7, 9]))
    # print(measures.euclidean_distance([1, 1, 0, 0], [1, 1, 1, -1]))


if __name__ == "__main__":
    main()
