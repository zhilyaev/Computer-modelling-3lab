import matplotlib.pyplot as plt
import numpy as np
import math
import random


class Part2:
    def __init__(self, t=50, y=0.7, separation=25, n=50, chi_squared=13.09051):
        # CONST
        self.T = t
        self.Y = y
        self.SEPARATION = separation
        self.N = n
        self.CHI_SQUARED = chi_squared
        # VARS
        self.x = np.arange(0, self.T, 0.1)
        self.y = [0] * self.T * 10
        self.separateY = [-1, 1]
        self.separateX = np.arange(0, self.T, self.T / self.SEPARATION)
        # Computing vars
        self.flow = self.flows2flow(self.generate())
        [self.countInRange, self.uniqueList] = self.catch_in_interval()
        self.lambda_t = sum(self.flow) / sum(self.countInRange)
        self.theoreticalN = self.theoretical()

    # Генерим из первой части 50 потоков
    def generate(self):
        iterations = []

        for i in range(0, self.T):
            t = 0
            i = 0
            times = []
            while t < self.T:
                y = random.uniform(0, 1)
                x = math.log((1 - y), math.e) / (-self.Y)
                u = x
                t += u
                i += 1

                if t < self.T:
                    rounded_t = round(t, 1)
                    if rounded_t not in times:
                        times.append(rounded_t)

            iterations.append(times)

        return iterations

    # Картинка
    def figure(self):
        plt.plot(self.x, self.y)
        for sepX in self.separateX:
            plt.plot([sepX] * 2, self.separateY)

        plt.margins(0, 5)
        plt.ylabel('y')
        plt.xlabel('x')

        plt.plot(self.flow, [0] * len(self.flow), 'ro', markersize=2)
        plt.show()

    # Получаем количество попаданий в интервал
    def catch_in_interval(self):
        # Левая границы
        left = 0
        # Правая границы
        right = left + self.T / self.SEPARATION
        # Уникальные
        u = None
        # Число попаданий
        c = []

        for i in range(0, self.SEPARATION):
            c.append(len(list(filter(lambda x: left < x < right, self.flow))))
            u = list(range(0, 10))

            # Переход к следующему отрезку
            # левая стала правой
            left = right
            # Правая
            right = left + self.T / self.SEPARATION

            self.flow[:] = [f / 10 for f in self.flow]

        return [c, u]

    # Все в один поток
    @staticmethod
    def flows2flow(iterations):
        a = []
        for x in iterations:
            a += x
        return a

    # Получаем n теоритическое
    def theoretical(self):
        n_theories = []
        n_sum = sum(self.countInRange)

        for n in self.uniqueList:
            p = pow(self.lambda_t, n) / math.factorial(n) * pow(math.e, -self.lambda_t)
            n_theories.append(p * n_sum)

        self.uniqueList[:] = [n - n / self.SEPARATION for n in n_theories]
        return n_theories

    # Получаем хи квадрат
    def chi_squared(self):
        chi = 0
        for count, n in zip(self.uniqueList, self.theoreticalN):
            chi += pow((count - n), 2) / n
        return chi

    def hypothesis(self):
        return self.chi_squared() < self.CHI_SQUARED


laba3 = Part2()
# print(laba3.flow)
print('lambda теориритическое: ' + str(laba3.lambda_t))
print('N теоритическое: ' + str(laba3.theoreticalN))
print('Хи квадрат: ' + str(laba3.chi_squared()))
if laba3.hypothesis():
    print('Гипотеза о пуассоновском потоке принимается')
else:
    print('Гипотеза о пуассоновском потоке отвергается')
laba3.figure()