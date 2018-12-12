import matplotlib.pyplot as plt
import numpy as np
import math
import random

T = 50
Y = 0.7
SEPARATION = 25
N = 50
X2_KRIT = 13.09051

x = np.arange(0, T, 0.1)
y = [0] * T * 10

separateY = [-1, 1]
separateX = np.arange(0, T, T / SEPARATION)


# Рисуем график
def draw():
    plt.plot(x, y)
    for sepX in separateX:
        plt.plot([sepX] * 2, separateY)

    plt.margins(0, 5)
    plt.ylabel('y')
    plt.xlabel('x')


# Рисуем точки
def drawDots(flow):
    plt.plot(flow, [0] * len(flow), 'ro', markersize=1)
    plt.show()


# Получаем общий поток
def getAllFlows(iterations):
    a = []
    for xArray in iterations:
        a += xArray

    return a


# Генерируем 50 потоков
def generate(T = T):
    lambdas = []

    for i in range(0, T):
        t = 0
        i = 0
        times = []
        while t < T:
            y = random.uniform(0, 1)
            x = math.log((1 - y), math.e) / (-Y)
            u = x
            t += u
            i += 1

            if t < T:
                roundedT = round(t, 1)
                if roundedT not in times:
                    times.append(roundedT)

        k = i + 1
        lambdas.append(times)

    return lambdas


# Получаем хи квадрат
def getX2(uniqeList, nTheors):
    # (c - n)^2 / n
    X = 0

    for count, n in zip(uniqeList, nTheors):
        X += pow((count - n), 2) / n

    print("X^2: ", X)
    return X


# получаем количество попаданий в интервал
def getCountInRange(flow):
    leftRange = 0
    rightRange = leftRange + T / SEPARATION

    countInRange = []

    for i in range(0, SEPARATION):
        listInRange = list(filter(lambda x: leftRange < x < rightRange, flow))
        countInRange.append(len(listInRange))
        uniqeList = list(range(0, 10))

        leftRange = rightRange
        rightRange = leftRange + T / SEPARATION

    flow[:] = [f / 10 for f in flow]

    print("count in range: ", uniqeList)
    return [countInRange, uniqeList]


# Получаем n теоритическое
def getNTheor(flow, countInRange, uniqeList):
    nTheors = []
    nSum = sum(countInRange)
    lambdaT = getLambdaT(flow, countInRange)

    for n in uniqeList:
        p = pow(lambdaT, n) / math.factorial(n) * pow(math.e, -lambdaT)
        nTheor = p * nSum
        nTheors.append(nTheor)
    uniqeList[:] = [n - n / SEPARATION for n in nTheors]
    print("n theors: ", nTheors)
    return nTheors


def getLambdaT(flow, countsInRange):
    ldt = sum(flow) / sum(countsInRange)
    print('λ∆t:', ldt)
    return ldt


iterations = generate()
allFlow = getAllFlows(iterations)
draw()
drawDots(allFlow)
[countInRange, uniqeList] = getCountInRange(allFlow)
nTheors = getNTheor(allFlow, countInRange, uniqeList)
X2 = getX2(uniqeList, nTheors)

if (X2 < X2_KRIT):
    print('Гипотеза о пуассоновском потоке принимается')
else:
    print('Гипотеза о пуассоновском потоке отвергается')
