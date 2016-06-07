import numpy as np
import sys
import math

lines = open("/media/DATA/Training/IBUG/IBUG/IBUG(13 features)-dataset.csv").read().split("\n")
lines = lines[1:]

ldata = []
for line in lines:
    if line != "":
        ldata.append(np.fromstring(line, sep=",", dtype=np.float64))

# print(ldata)
lneutral = []

for line in ldata:
    print(line[0])
    if line[0] == 0.0:
        lneutral.append(line[1:])

res = ""

lneutral = np.array(lneutral)

lneutral = lneutral.transpose()

for line in lneutral:
    res += str(np.mean(line, dtype=np.float64)) + ","

res = res[:-2]
file = open("/media/DATA/Training/IBUG/IBUG/neutral.csv", "w")
file.write(res)