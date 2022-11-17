# Your implementation should work on any dataset in the following format:

# The first line contains three numbers n, d, and r,
# where n is the number of points, d is the dimensionality
# of the instance space, and r is the radius.

# The i-th line (where i goes from 2 to n + 1) gives the (i - 1)-th point
# in the dataset as: x1,x2,...,xd,label

# where the first d values are the coordinates of the point, and label = 1 or -1.

import numpy as np
import math
import copy


def readData(filename):     # save data as numpy array
    data = np.loadtxt( filename, skiprows=1, delimiter=',')        # skip the first line
    #print(data)
    return data

def readFirstLine(filename):
    with open(filename) as f:
        fl = f.readline().strip('\n')
        fl = fl.split(',')
        f.close()
    firstLine = np.array(fl)
    #print(firstLine)
    return firstLine

# scan whole dataset to find a violation point and return a new w
def findViolation(w, r):
    wnew = copy.deepcopy(w)
    for i in range(1,n):      # every point
        molecular = 0        # calculate w*p
        denominator = 0
        for j in range(d):      # every dimension
            molecular = molecular+dataSet[i][j]*wnew[j]
            denominator = denominator+wnew[j]**2
        lable = dataSet[i][d]
        distance = abs(molecular)/np.sqrt(denominator)
        if np.sign(molecular) != lable or distance <= r/2:      # find one violation point
            for k in range(d):
                wnew[k] = wnew[k]+lable*dataSet[i][k]     # refresh w
            #print(wnew)
            return wnew
    return w


def termination(w,t,rguess):
    flag=0
    wnew = findViolation(w, rguess)
    for i in range(t):
        if (w==wnew).all()==True:
            flag=1
            break
        else:
            w = wnew
            wnew = findViolation(w,rguess)
    return flag,w,rguess


def marginPerceptron(R,rguess):
    w = dataSet[0][0:d] * dataSet[0][d]  # the first point of the data set must be a violaiton point
    t = math.ceil((12 * (R ** 2)) / (rguess ** 2))
    while termination(w,t,rguess)[0]!=1:
        w = dataSet[0][0:d] * dataSet[0][d]  # the first point of the data set must be a violaiton point
        rguess = rguess/2
        t = math.ceil((12 * (R ** 2)) / (rguess ** 2))
        termination(w,t,rguess)
    return termination(w,t,rguess)[1],termination(w,t,rguess)[2]


def findMargin(w,d,R):
    margin = R
    for i in range(1,n):      # every point
        molecular = 0        # calculate w*p
        denominator = 0
        for j in range(d):      # every dimension
            molecular = molecular+dataSet[i][j]*w[j]
            denominator = denominator+w[j]**2
        distance = abs(molecular)/np.sqrt(denominator)
        if distance<margin:
            margin = distance
    return margin



if __name__=="__main__":
    string = ['d2r16n10000.txt','d4r24n10000.txt','d8r12n10000.txt']
    for name in string:
        print("---------- Dataset: "+name+" ----------")
        dataSet = readData(name)
        firstLine = readFirstLine(name)
        R = int(firstLine[2])  # radius
        rguess = R  # original gamma guess
        print("original gamma guess: " + str(R))
        d = int(firstLine[0])  # d is the dimensionality of the instance space
        n = int(firstLine[1])  # n is the number of points
        result = marginPerceptron(R, rguess)
        print("gamma: " + str(result[1]))
        print("weight: " + str(result[0]))
        print("minimal margin: " + str(findMargin(result[0], d, R)))
        print('\n')



