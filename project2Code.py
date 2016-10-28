from math import exp, log
from statistics import stdev

def dictionary(file):
    dict = {}
    with open(file) as data:
        for line in data:
            x = float(line.split()[0])
            y = float(line.split()[1])
            dict[x] = y
    return(dict)

def maxOffset(dict):
	offset = 0
	for item in dict:
		if item < 0:
			if abs(item) > offset:
				offset = abs(item)
	return(offset)
	
    
def residualStDev(dict, type, a0, a1):
    residList = []
    for item in dict:
        x = item
        y = dict[item]
        if type == 'linear':
            yPrediction = a0 + (a1 * x)
            residList.append(y - yPrediction) 
        elif type == 'exponential':
            yPrediction = exp(a0 + (a1 * x))
            residList.append(y - yPrediction) 
        elif type == 'power':
            yPrediction = exp(a0) * (x ** a1)
            residList.append(y - yPrediction) 
    stDev = stdev(residList)
    return(stDev)

def regression(dict, type):
    # figure out the linear regression
    n = 0
    sumx = 0
    sumy = 0
    sumxy = 0
    sumx2 = 0
    for item in dict:
        if type == 'linear':
            x = item
            y = dict[x]           
        elif type == 'exponential':
            x = item
            y = log(dict[x])
        elif type == 'power':
            x = log(item)
            y = log(dict[item])
        n += 1
        sumxy += x * y
        sumx += x
        sumy += y
        sumx2 += x ** 2
    a0 = (sumy * sumx2 - sumx * sumxy) / (n * sumx2 - sumx * sumx)
    a1 = (n * sumxy - sumx * sumy) / (n * sumx2 - sumx * sumx)
    return(a0, a1)
 
def cleaner(dict, type, coeff):
    a0 = coeff[0]
    a1 = coeff[1]
    cleanDataDict = {}
    dirtyData = {}
    stDev = residualStDev(dict, type, a0, a1)
    offset = maxOffset(dict)
    for item in dict:
        x = item + offset
        y = dict[item]
        if type == "linear":
            yPrediction = a0 + (a1 * x)
            if abs(y - yPrediction) < 2 * stDev:
                cleanDataDict[x] = y
            else:
                dirtyData[x] = y
        elif type == "exponential":
            yPrediction = exp(a0 + (a1 * x))
            if abs(y - yPrediction) < 2 * stDev:
                cleanDataDict[x] = y
            else:
                dirtyData[x] = y
        elif type == "power":
            yPrediction = exp(a0) * (x ** a1)
            if abs(y - yPrediction) < 2 * stDev:
                cleanDataDict[x] = y
            else:
                dirtyData[x] = y
    print("Dirty Data: ", type, " : ", dirtyData)
    return(cleanDataDict)
   
def coefficients():
    volume = input('Input part volume in cm^3: ')
    tolerance = input('Input part tolerance in mm: ')
    speedCoeffs = regression(cleaner(dictionary('project2Speed.txt'),
        'linear', regression(dictionary('project2Speed.txt'), 'linear')), "linear")
    apertureCoeffs = regression(cleaner(dictionary('project2Aperture.txt'), 
        'exponential', regression(dictionary('project2Aperture.txt'), 'exponential')), "exponential")
    temperatureCoeffs = regression(cleaner(
        dictionary('project2Temperature.txt'), 'power', regression(dictionary(
            'project2Temperature.txt'), 'power')), "power")
    print("Speed Coefficients: ", speedCoeffs)
    print("Aperature Coefficients: ", apertureCoeffs)
    print("Temperature Coefficients: ", temperatureCoeffs)
    

coefficients()
   
#residualStDev(dictionary('project2Speed.txt'), 'linear', regression(dictionary('project2Speed.txt'), 'linear')[0], regression(dictionary('project2Speed.txt'), 'linear')[1])