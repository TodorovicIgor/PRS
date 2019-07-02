import numpy


def solveGN(k):
    '''
    p00=0, p01=0.15, p02=0.15, p0[range(3, k+4)]=0.7/k
    p10=0.5, p11=0, p12=0, p1[range(3, k+4)]=0.5/k
    p20=0.5, p21=0, p22=0, p2[range(3, k+4)]=0.5/k
    p[range 3, k+4]0=1, p[range 3, k+4]*=0

    '''
    mi0 = 1/0.005
    mi1 = 1/0.012
    mi2 = 1/0.015
    mi_d = 1/0.02

    coeff_matrix = []
    first_row = [0.5*mi1, 0.5*mi2]
    for i in range(k):
        first_row.append(mi_d)
    coeff_matrix.append(first_row)
    for i in range(k+1):
        row = []
        for j in range(k+2):
            if i>=2 and j<2:
                if j==0:
                    row.append((0.5/k)*mi1)
                if j==1:
                    row.append((0.5/k)*mi2)
                continue
            if i == j :
                if j==0:
                    row.append(-1*mi1)
                    continue
                if j==1:
                    row.append(-1*mi2)
                    continue
                row.append(-1*mi_d)
                continue
            row.append(0)

        coeff_matrix.append(row)

    # testing
    for i in coeff_matrix:
        print(i)

    ordinate = []
    ordinate.append(mi0)
    ordinate.append(-0.15*mi0)
    ordinate.append(-0.15*mi0)
    for i in range(k-1):
        ordinate.append((-0.7/k)*mi0)
    for i in ordinate:
        print(i)

    a = numpy.array(coeff_matrix)
    b = numpy.array(ordinate)
    solution = numpy.linalg.solve(a, b)
    ret = [1]
    for i in solution:
        ret.append(float(format_float(i)))
    return ret

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
    for i in range(len(G)):
        G[i] = float(format_float(G[i]))
    return float(format_float(G[len(G)-1]))


def get_j(x, n, index):
    G = [0] * len(x)
    G[0] = 1
    lastG = [1] * len(x)
    J = [1] * n
    for i in range(0, n):
        for j in range(1, len(x)):
            G[j] = G[j] * x[j] + G[j - 1]
            if j == index:
                J[i] = G[j]
                print(J[i])
    for j in range(1, len(x)):
        lastG[j] = G[j] * x[j] + lastG[j - 1]
        if j == index:
            J[n-1] = G[j]
        G[j] /= lastG[j]

    ret = 0
    for i in J:
        #print(J[i])
        print(i, G[index])
        ret += i/lastG[index]
    return ret


def exponential(b):
    return numpy.random.exponential(b)


def random():
    return numpy.random.random()


def format_float(value):
    return "%.6f" % value
'''
x = [1,1,2]
n=6
print(solveB(x, n))
'''
