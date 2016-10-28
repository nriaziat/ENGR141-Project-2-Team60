import math
from statistics import stdev

def dictionary(file):
    dict = {}
    with open(file) as data:
        for line in data:
            x = float(line.split()[0])
            y = float(line.split()[1])
            dict[x] = y
    return(dict)
    
def cleaner(file, type, a1, a0):
    residList = []
    with open(file) as rawData:
        for line in rawData:
            if type == 'linear':
                x = float(line.split()[0])
                y = float(line.split()[1])
                yPrediction = a0 + (a1 * x)
                residList.append(y - yPrediction) 
    stDev = stdev(residList, None)
    return(stDev)

def dataHandling (file, type):
    # figure out the linear regression
    cleanDataList = {}
    n = 0
    sumx = 0
    sumy = 0
    sumxy = 0
    sumx2 = 0
    with open(file) as rawData:
        for line in rawData:
            if type == 'linear':
                x = float(line.split()[0])
                y = float(line.split()[1])
            elif type == 'exponential':
                x = float(line.split()[0])
                y = math.log(float(line.split()[1]))
            elif type == 'power':
                x = math.log(float(line.split()[0]))
                y = math.log(float(line.split()[1]))
            n += 1
            sumxy += x * y
            sumx += x
            sumy += y
            sumx2 += x ** 2
    # file closed
    a0 = (sumy * sumx2 - sumx * sumxy) / (n * sumx2 - sumx * sumx)
    a1 = (n * sumxy - sumx * sumy) / (n * sumx2 - sumx * sumx)
    stDev = cleaner(file, type, a1, a0)
    with open(file) as rawData:
        for line in rawData:
            if type == "linear":
                x = float(line.split()[0])
                y = float(line.split()[1])
                yPrediction = a0 + (a1 * x)
                if abs(y - yPrediction) < 2 * stDev:
                    cleanDataList[x] = y
    print(cleanDataList)
                    
def main ():
    volume = input('Input part volume in cm^3: ')
    tolerance = input('Input part tolerance in mm: ')
    speedCoeffs = dataHandling('project2Speed.txt', 'linear')
    apertureCoeffs = dataHandling('project2Aperture.txt', 'exponential')
    temperatureCoeffs = dataHandling('project2Temperature.txt', 'power')
    """print(speedCoeffs)
    print(apertureCoeffs)
    print(temperatureCoeffs)
    print(math.exp(apertureCoeffs[0]))
    print(math.exp(temperatureCoeffs[0]))"""

    
main()






'''
        for line in rawData:
            speed = float(line.split()[0])
            error = float(line.split()[1])
            print('%f, %f' %(speed, error))
            sumyx += speed * error
            sumx2 += speed ** 2
        pretty much a test to make sure things work'''
