import math


def g(pozition):
    size = 4
    divisor = (int(math.log10(size)) + 1)*10
    xPozition = pozition // divisor -1
    yPozition = pozition % divisor -1
    print (xPozition,yPozition)

g(32)
g(24)