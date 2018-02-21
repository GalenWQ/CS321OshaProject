from k_means import *
import random

from dec_tree import (make_decision_tree, test_tree)


def read_data(file_name):
    data = []
    with open(file_name, "r") as data_file:
        for line in data_file:
            split_line = line.split()
            if split_line[0] != "HeatMiser_ID":
                if split_line[4] == 'Non-Compliant':
                    split_line[4] = 'NonCompliant'
                data.append(split_line)

    return data


# def findMax(data, column):
#     max = 0
#     for item in data:
#         val = float(item[column])
#         if val > max:
#             max = val
#
#     return max

def bin_data(data):
    # maxDistance = int(findMax(data, 1)) + 1
    #
    # while maxDistance % distanceBins != 0:
    #     maxDistance += 1
    #
    # distanceSplit = maxDistance / distanceBins
    #
    # maxSpeed = int(findMax(data, 2)) + 1
    #
    # while maxSpeed % speedBins != 0:
    #     maxSpeed += 1
    #
    # speedSplit = maxSpeed / speedBins

    for entry in data:
        # for i in range(int(distanceSplit), int(maxDistance) + 1,
        #                int(distanceSplit)):
        #     if float(entry[1]) <= i:
        #         entry[1] = "<" + str(i)
        #         break
        #
        # for i in range(int(speedSplit), int(maxSpeed) + 1,
        #                int(speedSplit)):
        #     if float(entry[2]) <= i:
        #         entry[2] = "<" + str(i)
        #         break

        if float(entry[1]) < 100:
            entry[1] = 'Short'
        else:
            entry[1] = 'Long'

        if int(entry[2]) < 10:
            entry[2] = '<10'
        elif int(entry[2]) < 20:
            entry[2] = '<20'
        elif int(entry[2]) < 30:
            entry[2] = '<30'
        elif int(entry[2]) < 40:
            entry[2] = '<40'
        elif int(entry[2]) < 50:
            entry[2] = '<50'
        elif int(entry[2]) < 60:
            entry[2] = '<60'
        elif int(entry[2]) < 70:
            entry[2] = '<70'
        else:
            entry[2] = '>70'

    return ['Short', 'Long'], ['<10', '<20', '<30', '<40', '<50', '<60', '<70', '>70'], ['Office', 'Warehouse']


def split_fold(data, fold):
    test_data = []
    learning_data = []

    lower_bound = (fold * len(data)) / 10
    upper_bound = ((fold + 1) * len(data)) / 10

    # print(lower_bound, upper_bound)

    for entry in data:
        if lower_bound <= data.index(entry) < upper_bound:
            test_data.append(entry)
        else:
            learning_data.append(entry)

    return test_data, learning_data


def main():
    data = read_data("HW3_Data.txt")
    speed_categories, distance_categories, location_categories = bin_data(data)
    categories = [0, speed_categories, distance_categories, location_categories]
    random.shuffle(data)

    # test_data, learning_data = split_fold(data, 6)
    #
    # root = make_decision_tree(learning_data, categories)
    # test_tree(test_data, root)

    average_results = {'safe_precision': 0, 'safe_recall': 0, 'safe_f1': 0,
                       'compliant_precision': 0, 'compliant_recall': 0, 'compliant_f1': 0,
                       'noncompliant_precision': 0, 'noncompliant_recall': 0,
                       'noncompliant_f1': 0, 'average_precision': 0, 'average_recall': 0,
                       'average_f1': 0, 'overall_precision': 0, 'majority_count': 0}

    for fold in range(10):
        print("\nFOLD", fold + 1)
        test_data, learning_data = split_fold(data, fold)

        root = make_decision_tree(learning_data, categories)
        results = test_tree(test_data, root)

        for key in average_results:
            average_results[key] += results[key]

    for key in average_results:
        average_results[key] /= 10

    print("\nAVERAGE OF ALL FOLDS")
    print('______________________________________________________')
    print("Precision (safe):", average_results['safe_precision'])
    print("Recall (safe):", average_results['safe_recall'])
    print("F1 (safe):", average_results['safe_f1'])
    print('-----------------------')
    print("Precision (compliant):", average_results['compliant_precision'])
    print("Recall (compliant):", average_results['compliant_recall'])
    print("F1 (compliant):", average_results['compliant_f1'])
    print('-----------------------')
    print("Precision (noncompliant):", average_results['noncompliant_precision'])
    print("Recall (noncompliant):", average_results['noncompliant_recall'])
    print("F1 (noncompliant):", average_results['noncompliant_f1'])
    print('-----------------------')
    print("Precision (average):", average_results['average_precision'])
    print("Recall (average):", average_results['average_recall'])
    print("F1 (average):", average_results['average_f1'])
    print('-----------------------')
    print("Precision (overall):", average_results['overall_precision'])
    print('______________________________________________________')

    data = read_data("HW3_Data.txt")
    random.shuffle(data)

    print(find_elbow(data))

    for fold in range(10):
        test_data, learning_data = split_fold(data, fold)

        clusters = build_clusters(learning_data, 3)


if __name__ == '__main__':
    main()
