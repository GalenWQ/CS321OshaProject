import math
import random

class Node:
    """A class representing a node in the decision tree."""

    def __init__(self, value):
        self.parent = None
        self.value = value
        self.children = []

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

    def addPossibleChildren(self, categories):
        column = self.value

        for feature in categories[column]:
            child = Node(feature)
            self.addChild(child)

    def __str__(self):
        return str(self.value)

def readData():
    data = []
    with open("HW3_Data.txt", "r") as dataFile:
        for line in dataFile:
            splitLine = line.split()
            if splitLine[0] != "HeatMiser_ID":
                data.append(splitLine)

    return data

# def findMax(data, column):
#     max = 0
#     for item in data:
#         val = float(item[column])
#         if val > max:
#             max = val
#
#     return max

def binData(data):
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

    return ['Short', 'Long'], ['<10', '<20', '<30', '<40', '<50', '<60',
                               '<70', '>70'], ['Office', 'Warehouse']

def splitFold(data, fold):
    testData = []
    learningData = []

    lowerBound = (fold * len(data)) / 10
    upperBound = ((fold + 1) * len(data)) / 10

    for entry in data:
        if lowerBound <= data.index(entry) < upperBound:
            testData.append(entry)
        else:
            learningData.append(entry)

    return testData, learningData

def H(vals):
    total = sum(vals)

    acc = 0
    for i in vals:
        percent = i / total
        if percent != 0:
            acc += percent * math.log2(percent)

    return -1 * acc

def findBaseline(data):
    safeCount = 0
    compliantCount = 0
    nonCompliantCount = 0

    for entry in data:
        if entry[4] == 'Safe':
            safeCount += 1
        elif entry[4] == 'Compliant':
            compliantCount += 1
        elif entry[4] == 'NonCompliant' or entry[4] == 'Non-Compliant':
            nonCompliantCount += 1
        else:
            print("ERROR: incorrectly formatted compliance value", entry[4])
            quit()

    total = safeCount + compliantCount + nonCompliantCount
    safePercent = safeCount / total
    compliantPercent = compliantCount / total
    nonCompliantPercent = nonCompliantCount / total

    return max(safePercent, compliantPercent, nonCompliantPercent)

def itemInScope(node, item):
    curNode = node
    while curNode is not None:
        feature = node.value
        column = node.parent.value
        if item[column] != feature:
            return False
        else:
            curNode = curNode.parent.parent

    return True

def columnInScope(node, column):
    curNode = node
    while curNode is not None:
        nextColumn = curNode.parent.value
        if column == nextColumn:
            return False
        else:
            curNode = curNode.parent.parent

    return True

def calculateEntropy(data, node=None):
    safeCount = 0
    compliantCount = 0
    nonCompliantCount = 0

    for entry in data:
        if itemInScope(node, entry):
            if entry[4] == 'Safe':
                safeCount += 1
            elif entry[4] == 'Compliant':
                compliantCount += 1
            elif entry[4] == 'NonCompliant' or entry[4] == 'Non-Compliant':
                nonCompliantCount += 1

    entropy = H([safeCount, compliantCount, nonCompliantCount])

    return entropy

def calculateBestGuess(data, node):
    safeCount = 0
    compliantCount = 0
    nonCompliantCount = 0

    for entry in data:
        if itemInScope(node, entry):
            if entry[4] == 'Safe':
                safeCount += 1
            elif entry[4] == 'Compliant':
                compliantCount += 1
            elif entry[4] == 'NonCompliant' or entry[4] == 'Non-Compliant':
                nonCompliantCount += 1

    maximum = max(safeCount, compliantCount, nonCompliantCount)

    if maximum == safeCount:
        return 'Safe'
    elif maximum == compliantCount:
        return 'Compliant'
    else:
        return 'NonCompliant'

def findInfoGain(data, baselineEntropy, column, node=None):
    matrix = []

    possibilities = []
    for item in data:
        if itemInScope(node, item):
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

    return baselineEntropy - entropy

def findInfoGains(data, entropy, node=None):
    infoGains = [0]

    for column in range(1, 4):
        if columnInScope(node, column):
            infoGain = findInfoGain(data, entropy, column, node)
            infoGains.append(infoGain)
        else:
            infoGains.append(0)

    return infoGains

def findNextColumn(data, entropy, node=None):
    infoGains = findInfoGains(data, entropy, node)
    maxInfoGain = max(infoGains)
    nextColumn = infoGains.index(maxInfoGain)

    return nextColumn

def addBranches(data, root, depth, categories):
    root.addPossibleChildren(categories)

    for node in root.children:
        entropy = calculateEntropy(data, node)

        if entropy == 0 or depth > 2:
            result = calculateBestGuess(data, node)
            child = Node(result)
            node.addChild(child)
        else:
            nextColumn = findNextColumn(data, entropy, node)

            child = Node(nextColumn)
            node.addChild(child)
            addBranches(data, child, depth + 1, categories)

def printTree(root, indent):
    print("\t" * indent, root)
    if root:
        for child in root.children:
            printTree(child, indent + 1)

def testTree(testData, root):
    correct = 0
    incorrect = 0

    for item in testData:
        curNode = root

        while curNode.children:
            category = item[curNode.value]
            for child in curNode.children:
                if category == child.value:
                    curNode = child.children[0]

        prediction = curNode.value
        if prediction == item[4]:
            correct += 1
        else:
            incorrect += 1

    return correct, incorrect

def main():
    data = readData()
    speedCategories, distanceCategories, locationCategories = binData(data)
    categories = [0, speedCategories, distanceCategories, locationCategories]
    random.shuffle(data)

    for fold in range(10):
        testData, learningData = splitFold(data, fold)

        entropy = calculateEntropy(learningData)

        nextColumn = findNextColumn(learningData, entropy)
        root = Node(nextColumn)

        addBranches(learningData, root, 1, categories)

        #printTree(root, 0)

        correct, incorrect = testTree(testData, root)
        majorityCount = findBaseline(testData)

        print("majority count:", majorityCount)
        print("correct percentage:", correct / (correct + incorrect))
        print("________________________________________________________")


if __name__ == '__main__':
    main()
