import numpy as np
def postDataProcess(crit1Expectation):
    crit1Expectation = [[['{:.2f}'.format(x) for x in item] for item in sublist] for sublist in crit1Expectation]
    for rowIdx, earlyDiscard in enumerate(earlyDiscards):
        print("Discard if no double crit after first " + str(earlyDiscard + 1))
        for col in range(crit1DiscardChecks):
            print("Discard if no crit after " + str(col + 1), crit1Expectation[rowIdx][col])
        print("\n")
    print(crit1Expectation)

    data = [[[float(item[0]), float('{:.2f}'.format(float(item[1]) / 10)), float(item[2])] for item in sublist] for
            sublist in crit1Expectation]

    newData = [[0 for col in range(3)] for row in range(16)]
    for row in range(len(data)):
        for col in range(len(data[0])):
            for type in range(3):
                newData[row * 4 + col][type] = data[row][col][type]

    for row in newData:
        print(row, '\n')

    # csv = ''
    # csv += '2总1单,2总2单,2总3单,2总4单,3总1单,3总2单,3总3单,3总4单,4总1单,4总2单,4总3单,4总4单,5总1单,5总2单,5总3单,5总4单\n'

    csv = '经验(万), 打孔器/10, 胚子(个)\n'
    for row in newData:
        for val in row:
            csv += str(val) + ', '
        csv = csv[:len(csv) - 2]
        csv += "\n"
    with open('wutheringwave.csv', 'w') as file:
        file.write(csv)

EXP_REUSE = 0.75
HOLE_REUSE = 0.3

weights = [1 / 13 for i in range(13)]
cards = [i for i in range(13)]  # card[0] is critrate, card[1] is critdmg

expDiff = [0.45, 1.2, 2.3, 4, 6.4]
expAccu = [0.45, 1.65, 3.95, 7.95, 14.35]

# targetAmount = 5
targetAmount = 10000

crit1DiscardChecks = 4

earlyDiscards = [1, 2, 3, 4]
# earlyDiscards = [4]

crit1Expectation = [[-1 for col in range(4)] for row in range(len(earlyDiscards))]

echo = None



for idx, earlyDiscard in enumerate(earlyDiscards):
    for discard_idx in range(crit1DiscardChecks):
        expHistory = [-1] * targetAmount
        holeHistory = [-1] * targetAmount
        embryoHistory = [-1] * targetAmount
        for t in range(targetAmount):
            # print("t:", t)
            embryo = 1
            echo = np.random.choice(cards, size=5, replace=False, p=weights).tolist()
            expTotal = curExp = expAccu[discard_idx]
            holeTotal = curHole = 10 * (discard_idx + 1)

            doubleCRIT = False

            while not doubleCRIT:
                while 0 not in echo[0:discard_idx + 1] and 1 not in echo[0:discard_idx + 1]:
                    echo = np.random.choice(cards, size=5, replace=False, p=weights).tolist()
                    embryo += 1
                    curExp -= expAccu[discard_idx] * (1 - EXP_REUSE)
                    curHole -= 10 * (discard_idx + 1) * (1 - HOLE_REUSE)
                    expDiff = max(0.0, expAccu[discard_idx] - curExp)
                    holeDiff = max(0, 10 * (discard_idx + 1) - curHole)

                    expTotal += expDiff
                    curExp += expDiff
                    holeTotal += holeDiff
                    curHole += holeDiff

                # if passed 1 crit, then increase to checkLevel
                checkLevel = max(discard_idx + 1, earlyDiscard)
                expTotal += expAccu[checkLevel] - curExp
                holeTotal += 10 * (checkLevel + 1) - curHole
                curExp = expAccu[checkLevel]
                curHole = 10 * (checkLevel + 1)
                curExp -= expAccu[checkLevel] * (1 - EXP_REUSE)
                curHole -= 10 * (checkLevel + 1) * (1 - HOLE_REUSE)

                if 0 in echo[:checkLevel + 1] and 1 in echo[:checkLevel + 1]:
                    doubleCRIT = True
                    # increase to level 25
                    # expTotal += expAccu[4] - expAccu[checkLevel]
                    # holeTotal += 50 - (10 * (checkLevel + 1))
                else:
                    echo = np.random.choice(cards, size=5, replace=False, p=weights).tolist()
                    embryo += 1

            expHistory[t] = expTotal
            holeHistory[t] = holeTotal
            embryoHistory[t] = embryo

        expExpected = sum(expHistory) / targetAmount
        holeExpected = sum(holeHistory) / targetAmount
        embryoExpected = sum(embryoHistory) / targetAmount

        # print("expHistory:", expHistory)
        # print("holeHistory:", holeHistory)
        # print("embryoHistory:", embryoHistory)
        # print("")
        #
        # print("expExpected:", expExpected)
        # print("holeExpected:", holeExpected)
        # print("embryoExpected:", embryoExpected)
        # print("")
        # print("")

        crit1Expectation[idx][discard_idx] = (
            # 'del1:' + str(discard_idx + 1) + ' del2:' + str(earlyDiscard + 1),
            expExpected, holeExpected, embryoExpected)


postDataProcess(crit1Expectation)