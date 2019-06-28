import Queue,Resources,random

print("Unesite stepen multiprogramiranja: ")
n = int(input())
CPU = Resources.CPU()
SDisc1 = Resources.SysDisc(12)
SDisc2 = Resources.SysDisc(15)
tasks = []
for i in range(0, n):
    Fifo.append(Resources.Task())

for k in range (2, 9):

