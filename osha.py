from dec_tree import *

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

    return ['Short', 'Long'], ['<10', '<20', '<30', '<40', '<50', '<60', '<70', '>70'], ['Office', 'Warehouse']

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


def main():
    data = readData()
    speedCategories, distanceCategories, locationCategories = binData(data)
    categories = [0, speedCategories, distanceCategories, locationCategories]
    random.shuffle(data)

    for fold in range(10):
        testData, learningData = splitFold(data, fold)

        root = makeDecisionTree(learningData, categories)
        testTree(testData, root)


if __name__ == '__main__':
    main()
