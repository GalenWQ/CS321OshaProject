from k_means import (build_clusters, eval_clusters, test_clusters, find_elbow)
import random

from dec_tree import (make_decision_tree, test_tree)
import pandas as pd
from plotting import ClusterPlotter


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


def bin_data(data):
    for entry in data:
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

    average_results = {'safe_precision': 0, 'safe_recall': 0, 'safe_f1': 0,
                       'compliant_precision': 0, 'compliant_recall': 0, 'compliant_f1': 0,
                       'noncompliant_precision': 0, 'noncompliant_recall': 0,
                       'noncompliant_f1': 0, 'average_precision': 0, 'average_recall': 0,
                       'average_f1': 0, 'overall_precision': 0, 'majority_count': 0}

    print("******************************************************")
    print("DECISION TREES")
    print("******************************************************")

    all_results = []

    for fold in range(10):
        print("\nFOLD", fold + 1)
        test_data, learning_data = split_fold(data, fold)

        root = make_decision_tree(learning_data, categories)
        results = test_tree(test_data, root)
        all_results.append(results)

        for key in average_results:
            average_results[key] += results[key]

        df = pd.DataFrame(all_results)
        df.to_json('all_results.json')

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

    # print(find_elbow(data))

    print("******************************************************")
    print("K-MEANS CLUSTERING")
    print("******************************************************")

    avg_accuracy = 0

    cp = ClusterPlotter()

    for fold in range(10):
        print("\nFOLD", fold + 1)
        test_data, learning_data = split_fold(data, fold)

        clusters = build_clusters(learning_data, 8)
        cp.add_cluster_list(clusters)

        eval_clusters(clusters)
        print('______________________________________________________')
        accuracy = test_clusters(clusters, test_data)
        avg_accuracy += accuracy

    avg_accuracy /= 10

    print('______________________________________________________')
    print("AVERAGE CLASSIFICATION ACCURACY ACROSS ALL FOLDS:", avg_accuracy)

if __name__ == '__main__':
    main()
