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

    def __str__(self):
        return str(self.value)


def H(vals):
    total = sum(vals)

    acc = 0
    for i in vals:
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
        elif entry[4] == 'NonCompliant' or entry[4] == 'Non-Compliant':
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


def calculateEntropy(data, node=None):
    safe_count = 0
    compliant_count = 0
    non_compliant_count = 0

    for entry in data:
        if item_in_scope(node, entry):
            if entry[4] == 'Safe':
                safe_count += 1
            elif entry[4] == 'Compliant':
                compliant_count += 1
            elif entry[4] == 'NonCompliant' or entry[4] == 'Non-Compliant':
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
            elif entry[4] == 'NonCompliant' or entry[4] == 'Non-Compliant':
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
            elif item[4] == 'NonCompliant' or item[4] == 'Non-Compliant':
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
        entropy = calculateEntropy(data, node)

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
    correct = 0
    incorrect = 0

    for item in test_data:
        cur_node = root

        while cur_node.children:
            category = item[cur_node.value]
            for child in cur_node.children:
                if category == child.value:
                    cur_node = child.children[0]

        prediction = cur_node.value
        if prediction == item[4]:
            correct += 1
        else:
            incorrect += 1

    majority_count = find_baseline(test_data)

    print("majority count:", majority_count)
    print("correct percentage:", correct / (correct + incorrect))
    print('-----------------------')


def make_decision_tree(learning_data, categories):
    entropy = calculateEntropy(learning_data)

    next_column = find_next_column(learning_data, entropy)
    root = Node(next_column)

    add_branches(learning_data, root, 1, categories)

    # printTree(root, 0)

    return root
