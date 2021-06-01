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


# from unicodedata import decimal
#
# import similaritymeasures
# from Similarity import *
# import csv
#
#
# def main():
#     """ main function to create Similarity class instance and get use of it """
#
#     measures = Similarity()
#
#     csv_reader = csv.reader(open("./reformat/000002.csv", 'r', encoding='gbk'))
#     n = 0
#     data_set_1 = []
#     for row in csv_reader:
#         if n == 0:
#             n += 1
#             continue
#         else:
#             n += 1
#             if row[4] == 'None':
#                 continue
#             data_set_1.append(float(row[4]))
#
#     csv_reader = csv.reader(open("./reformat/000004.csv", 'r', encoding='gbk'))
#     n = 0
#     data_set_2 = []
#     for row in csv_reader:
#         if n == 0:
#             n += 1
#             continue
#         else:
#             n += 1
#             # print(row[4])
#             if row[4] == 'None':
#                 continue
#             data_set_2.append(float(row[4]))
#     # print(data_set_2)
#     print(measures.jaccard_similarity(data_set_1, data_set_2))
#
#     # print(measures.euclidean_distance([0, 3, 4, 5], [7, 6, 3, -1]))
#     # print(measures.jaccard_similarity([0, 1, 2, 5, 6], [0, 2, 3, 5, 7, 9]))
#     # print(measures.euclidean_distance([1, 1, 0, 0], [1, 1, 1, -1]))
import time
from math import *
from dateutil import rrule
import matplotlib.pyplot as plt
import numpy
import csv
import json
import os
import os.path
import re
import sys
import codecs
from datetime import datetime


def print_matrix(mat):
    print('[matrix] width : %d height : %d' % (len(mat[0]), len(mat)))
    print('-----------------------------------')
    for i in range(len(mat)):
        print
        mat[i]  # [v[:2] for v in mat[i]]


def dist_for_float(p1, p2):
    dist = 0.0
    elem_type = type(p1)
    if elem_type == float or elem_type == int:
        dist = float(abs(p1 - p2))
    else:
        sumval = 0.0
        for i in range(len(p1)):
            sumval += pow(p1[i] - p2[i], 2)
        dist = pow(sumval, 0.5)
    return dist


def dtw(s1, s2, dist_func):
    w = len(s1)
    h = len(s2)

    mat = [([[0, 0, 0, 0] for j in range(w)]) for i in range(h)]

    # print_matrix(mat)

    for x in range(w):
        for y in range(h):
            dist = dist_func(s1[x], s2[y])
            mat[y][x] = [dist, 0, 0, 0]

    # print_matrix(mat)

    elem_0_0 = mat[0][0]
    elem_0_0[1] = elem_0_0[0] * 2

    for x in range(1, w):
        mat[0][x][1] = mat[0][x][0] + mat[0][x - 1][1]
        mat[0][x][2] = x - 1
        mat[0][x][3] = 0

    for y in range(1, h):
        mat[y][0][1] = mat[y][0][0] + mat[y - 1][0][1]
        mat[y][0][2] = 0
        mat[y][0][3] = y - 1

    for y in range(1, h):
        for x in range(1, w):
            distlist = [mat[y][x - 1][1], mat[y - 1][x][1], 2 * mat[y - 1][x - 1][1]]
            mindist = min(distlist)
            idx = distlist.index(mindist)
            mat[y][x][1] = mat[y][x][0] + mindist
            if idx == 0:
                mat[y][x][2] = x - 1
                mat[y][x][3] = y
            elif idx == 1:
                mat[y][x][2] = x
                mat[y][x][3] = y - 1
            else:
                mat[y][x][2] = x - 1
                mat[y][x][3] = y - 1

    result = mat[h - 1][w - 1]
    retval = result[1]
    path = [(w - 1, h - 1)]
    while True:
        x = result[2]
        y = result[3]
        path.append((x, y))

        result = mat[y][x]
        if x == 0 and y == 0:
            break

    # print_matrix(mat)

    return retval, sorted(path)


def display(s1, s2):
    val, path = dtw(s1, s2, dist_for_float)

    w = len(s1)
    h = len(s2)

    mat = [[1] * w for i in range(h)]
    for node in path:
        x, y = node
        mat[y][x] = 0

    mat = numpy.array(mat)

    plt.subplot(2, 2, 2)
    c = plt.pcolor(mat, edgecolors='k', linewidths=4000)
    plt.title('Dynamic Time Warping (%f)' % val)

    plt.subplot(2, 2, 1)
    plt.plot(s2, range(len(s2)), 'g')

    plt.subplot(2, 2, 4)
    plt.plot(range(len(s1)), s1, 'r')
    plt.savefig('./test.png')
    plt.show()


def try_1st():
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
    display(data_set_1, data_set_2)


def csv_to_json():
    path = './reformat/'
    files = os.listdir(path)
    data = []
    for file in files:
        # print(file.title())
        with open('./reformat/' + file.title(), encoding='gbk') as f:
            is_first = True
            dic = {}
            detailed = []
            for line in f:
                line = list(line.split(','))
                dict = {}
                if is_first:
                    is_first = False
                else:
                    dic['股票代码'] = line[0]
                    dic['名称'] = line[1]
                    # print(line[2])
                    # dict['开始日期'] = time.strptime(line[2], '%Y-%m-%d')
                    # dict['结束日期'] = time.strptime(line[3], '%Y-%m-%d')
                    dict['开始日期'] = line[2]
                    dict['结束日期'] = line[3]
                    if line[4] == 'None\n':
                        dict['涨幅'] = 0.0
                    else:
                        dict['涨幅'] = float(line[4])
                if dict != {}:
                    detailed.append(dict)
            dic['变动信息'] = detailed
        data.append(dic)
        print(dic)
    with open('./reformed_data.json', 'w', encoding='utf8') as f:
        json.dump(data, f)
    dic_from_json = open('./reformed_data.json', 'r')
    info_data = json.load(dic_from_json)
    with open('./reformed_data.json', "w", encoding='utf8') as ff:
        json.dump(info_data, ff, ensure_ascii=False)


def split_by_date():
    # data = []
    # dic_from_json = open('reformed_data.json', 'r')
    # info_data = json.load(dic_from_json)
    # print(type(info_data))
    string_test_1 = "2021-04-01"
    string_test_2 = "2021-06-01"
    time_1 = time.strptime(string_test_1, "%Y-%m-%d")
    time_2 = time.strptime(string_test_2, "%Y-%m-%d")
    # print(type(time_1.tm_mday))
    months = rrule.rrule(freq=rrule.MONTHLY, dtstart=datetime(time_1.tm_year, time_1.tm_mon, time_1.tm_mday), until=datetime(time_2.tm_year, time_2.tm_mon, time_2.tm_mday))
    print(months.count())

if __name__ == "__main__":
    # csv_to_json()
    split_by_date()
