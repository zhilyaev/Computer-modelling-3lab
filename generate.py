import math
import random


def generate(T=50, Y=0.7):
    lambdas = []
    for i in range(0, T):
        t = 0
        i = 0
        while t < T:
            y = random.uniform(0, 1)
            x = math.log((1 - y), math.e) / (-Y)
            u = x
            t += u
            i += 1

        k = i + 1
        lambdas.append(k / T)

    return 1 / T * sum(lambdas)


print(generate())
