import numpy

def solveGN():
    pass


def solveB(x, n):
    G = [0] * len(x)
    G[0] = 1
    lastG = [1] * len(x)
    for i in range(0, n):
        for j in range(1, len(x)):
           G[j] = G[j] * x[j] + G[j-1]
    for j in range(1, len(x)):
        lastG[j] = G[j] * x[j] + lastG[j-1]
        G[j] /= lastG[j]
    #print(lastG)
    return G


def exponential(b):
    return numpy.random.exponential(b)


def random():
    return numpy.random.random()