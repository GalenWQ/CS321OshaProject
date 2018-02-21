import math


class Node:
    """A class representing a node in the decision tree."""

    def __init__(self, value):
        self.parent = None
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def add_possible_children(self, categories):
        column = self.value

        for feature in categories[column]:
            child = Node(feature)
            self.add_child(child)

    def __repr__(self):
        return "Node: {}".format(self.value)


def H(vals):
    total = sum(vals)

    acc = 0
    for i in vals:
        if total != 0:
            percent = i / total
            if percent != 0:
                acc += percent * math.log2(percent)

    return -1 * acc


def find_baseline(data):
    safe_count = 0
    compliant_count = 0
    non_compliant_count = 0

    for entry in data:
        if entry[4] == 'Safe':
            safe_count += 1
        elif entry[4] == 'Compliant':
            compliant_count += 1
        elif entry[4] == 'NonCompliant':
            non_compliant_count += 1
        else:
            print("ERROR: incorrectly formatted compliance value", entry[4])
            quit()

    total = safe_count + compliant_count + non_compliant_count
    safe_percent = safe_count / total
    compliant_percent = compliant_count / total
    non_compliant_percent = non_compliant_count / total

    return max(safe_percent, compliant_percent, non_compliant_percent)


def item_in_scope(node, item):
    cur_node = node
    while cur_node is not None:
        feature = node.value
        column = node.parent.value
        if item[column] != feature:
            return False
        else:
            cur_node = cur_node.parent.parent

    return True


def column_in_scope(node, column):
    cur_node = node
    while cur_node is not None:
        next_column = cur_node.parent.value
        if column == next_column:
            return False
        else:
            cur_node = cur_node.parent.parent

    return True


def calculate_entropy(data, node=None):
    safe_count = 0
    compliant_count = 0
    non_compliant_count = 0

    for entry in data:
        if item_in_scope(node, entry):
            if entry[4] == 'Safe':
                safe_count += 1
            elif entry[4] == 'Compliant':
                compliant_count += 1
            elif entry[4] == 'NonCompliant':
                non_compliant_count += 1

    entropy = H([safe_count, compliant_count, non_compliant_count])

    return entropy


def calculate_best_guess(data, node):
    safe_count = 0
    compliant_count = 0
    non_compliant_count = 0

    for entry in data:
        if item_in_scope(node, entry):
            if entry[4] == 'Safe':
                safe_count += 1
            elif entry[4] == 'Compliant':
                compliant_count += 1
            elif entry[4] == 'NonCompliant':
                non_compliant_count += 1

    maximum = max(safe_count, compliant_count, non_compliant_count)

    if maximum == safe_count:
        return 'Safe'
    elif maximum == compliant_count:
        return 'Compliant'
    else:
        return 'NonCompliant'


def find_info_gain(data, baseline_entropy, column, node=None):
    matrix = []

    possibilities = []
    for item in data:
        if item_in_scope(node, item):
            if item[column] not in possibilities:
                possibilities.append(item[column])

            index = possibilities.index(item[column])

            if len(matrix) - 1 < index:
                matrix.append([0, 0, 0])

            if item[4] == 'Safe':
                matrix[index][0] += 1
            elif item[4] == 'Compliant':
                matrix[index][1] += 1
            elif item[4] == 'NonCompliant':
                matrix[index][2] += 1

    entropy = 0

    for feature in possibilities:
        index = possibilities.index(feature)
        num = sum(matrix[index])
        prob = num / len(data)
        entropy += prob * H([matrix[index][0], matrix[index][1], matrix[index][
            2]])

    return baseline_entropy - entropy


def find_info_gains(data, entropy, node=None):
    info_gains = [0]

    for column in range(1, 4):
        if column_in_scope(node, column):
            info_gain = find_info_gain(data, entropy, column, node)
            info_gains.append(info_gain)
        else:
            info_gains.append(0)

    return info_gains


def find_next_column(data, entropy, node=None):
    info_gains = find_info_gains(data, entropy, node)
    max_info_gain = max(info_gains)
    next_column = info_gains.index(max_info_gain)

    return next_column


def add_branches(data, root, depth, categories):
    root.add_possible_children(categories)

    for node in root.children:
        entropy = calculate_entropy(data, node)

        if entropy == 0 or depth > 2:
            result = calculate_best_guess(data, node)
            child = Node(result)
            node.add_child(child)
        else:
            next_column = find_next_column(data, entropy, node)

            child = Node(next_column)
            node.add_child(child)
            add_branches(data, child, depth + 1, categories)


def print_tree(root, indent):
    print("\t" * indent, root)
    if root:
        for child in root.children:
            print_tree(child, indent + 1)


def test_tree(test_data, root):
    actual_safe = 0
    safe_true_positive = 0
    safe_false_positive = 0
    safe_precision = 1.0
    safe_recall = 1.0
    safe_f1 = 1.0

    actual_compliant = 0
    compliant_true_positive = 0
    compliant_false_positive = 0
    compliant_precision = 1.0
    compliant_recall = 1.0
    compliant_f1 = 1.0

    actual_noncompliant = 0
    noncompliant_true_positive = 0
    noncompliant_false_positive = 0
    noncompliant_precision = 1.0
    noncompliant_recall = 1.0
    noncompliant_f1 = 1.0

    for item in test_data:
        cur_node = root

        while cur_node.children:
            category = item[cur_node.value]
            for child in cur_node.children:
                if category == child.value:
                    cur_node = child.children[0]

        prediction = cur_node.value

        if item[4] == 'Safe':
            actual_safe += 1
            if prediction == 'Safe':
                safe_true_positive += 1
            elif prediction == 'Compliant':
                compliant_false_positive += 1
            elif prediction == 'NonCompliant':
                noncompliant_false_positive += 1
        elif item[4] == 'Compliant':
            actual_compliant += 1
            if prediction == 'Safe':
                safe_false_positive += 1
            elif prediction == 'Compliant':
                compliant_true_positive += 1
            elif prediction == 'NonCompliant':
                noncompliant_false_positive += 1
        elif item[4] == 'NonCompliant':
            actual_noncompliant += 1
            if prediction == 'Safe':
                safe_false_positive += 1
            elif prediction == 'Compliant':
                compliant_false_positive += 1
            elif prediction == 'NonCompliant':
                noncompliant_true_positive += 1
        else:
            print("Something weird happened:", item[4])
            quit()

    if actual_safe > 0:
        if safe_true_positive + safe_false_positive > 0:
            safe_precision = safe_true_positive / (safe_true_positive + safe_false_positive)
        safe_recall = safe_true_positive / actual_safe
        safe_f1 = (2 * safe_recall * safe_precision) / (safe_recall + safe_precision)

    if actual_compliant > 0:
        if compliant_true_positive + compliant_false_positive > 0:
            compliant_precision = compliant_true_positive / (compliant_true_positive + compliant_false_positive)
        compliant_recall = compliant_true_positive / actual_compliant
        compliant_f1 = (2 * compliant_recall * compliant_precision) / (compliant_recall + compliant_precision)

    if actual_noncompliant > 0:
        if noncompliant_true_positive + noncompliant_false_positive > 0:
            noncompliant_precision = noncompliant_true_positive / (noncompliant_true_positive + noncompliant_false_positive)
        noncompliant_recall = noncompliant_true_positive / actual_noncompliant
        noncompliant_f1 = (2 * noncompliant_recall * noncompliant_precision) / (noncompliant_recall + noncompliant_precision)

    majority_count = find_baseline(test_data)

    overall_precision = (safe_true_positive + compliant_true_positive + noncompliant_true_positive) / len(test_data)
    average_precision = (safe_precision + compliant_precision + noncompliant_precision) / 3
    overall_recall = (safe_recall + compliant_recall + noncompliant_recall) / 3
    overall_f1 = (safe_f1 + compliant_f1 + noncompliant_f1) / 3

    print('______________________________________________________')
    print("Precision (safe):", safe_precision)
    print("Recall (safe):", safe_recall)
    print("F1 (safe):", safe_f1)
    print('-----------------------')
    print("Precision (compliant):", compliant_precision)
    print("Recall (compliant):", compliant_recall)
    print("F1 (compliant):", compliant_f1)
    print('-----------------------')
    print("Precision (noncompliant):", noncompliant_precision)
    print("Recall (noncompliant):", noncompliant_recall)
    print("F1 (noncompliant):", noncompliant_f1)
    print('-----------------------')
    print("Precision (average):", average_precision)
    print("Recall (average):", overall_recall)
    print("F1 (average):", overall_f1)
    print('-----------------------')
    print("Precision (overall):", overall_precision)
    print("Majority count:", majority_count)
    print('______________________________________________________')


def make_decision_tree(learning_data, categories):
    entropy = calculate_entropy(learning_data)

    next_column = find_next_column(learning_data, entropy)
    root = Node(next_column)

    add_branches(learning_data, root, 1, categories)

    # print_tree(root, 0)

    return root
