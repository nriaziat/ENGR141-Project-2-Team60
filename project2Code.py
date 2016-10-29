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
    #print("Dirty Data: ", type, " : \n", dirtyData)
    return(cleanDataDict)
   
def dataHandling(file, regType):
    data = dictionary(file)
    initialReg = regression(data, regType)
    initA0 = initialReg[0]
    initialA1 = initialReg[1]
    cleanData = cleaner(data, regType, initialReg)
    finalReg = regression(cleanData, regType)
    return(finalReg)
    
def coefficients():
    speedCoeffs = dataHandling('project2Speed.txt','linear')
    apertureCoeffs = dataHandling('project2Aperture.txt', 'exponential')
    temperatureCoeffs = dataHandling('project2Temperature.txt', 'power')
    return(speedCoeffs[0], speedCoeffs[1], apertureCoeffs[0], apertureCoeffs[1], temperatureCoeffs[0], temperatureCoeffs[1])

def inputs():
    volume = float(input("Enter print volume in cubic centimeters: "))
    tolerance = float(input("Enger print tolerance in centimeters: "))
    return(volume, tolerance)
    
def speedError(coefficients, headSpeed):
    a0 = coefficients[0]
    a1 = coefficients[1]
    speedError = a0 + a1 * headSpeed 
    return(speedError)

def apertureError(coefficients, aperture):
    a0 = coefficients[0]
    a1 = coefficients[1]
    apertureError = exp(a0 + (a1 * aperture))
    return(apertureError)

def temperatureError(coefficients, temp):
    a0 = coefficients[0]
    a1 = coefficients[1]
    temperatureError = exp(a0) * temp ** a1
    return(temperatureError)
    
def errorFunc(speedError, apertureError, temperatureError):
    error = speedError + apertureError + temperatureError
    return(error)
    
def printTime(volume, headSpeed, aperture):
    printingTime = volume / (headSpeed * aperture)
    return(printingTime)
    
def cureTime(temp):
    if temp >= 4 and temp <= 36:
        cureTime = 1570 / temp + 20 
    else:
        cureTime = 10000000
    return(cureTime)

def productionTime(printingTime, cureTime):
    if printingTime >= cureTime:
        prodTime = printingTime + 20
    elif printingTime < cureTime:
        prodTime = cureTime
    return(prodTime)
    
def costFunc(volume, productionTime):
    c = 500 * volume + 18 * productionTime
    return(c)

def minimize(constraint, coefficients):
    volume = constraint[0]
    tolerance = constraint[1]
    n = 0 
    temp = 4
    aperture = .01
    headSpeed = .5
    cost = 10000000
    error = 10000000
    speedCoeffs = coefficients[0:2]
    apertureCoeffs = coefficients[2:4]
    temperatureCoeffs = coefficients[4:6]
    while n < 1000:
        costNew = costFunc(volume, productionTime(printTime(volume, headSpeed, aperture), cureTime(temp)))
        errorNew =  errorFunc(speedError(speedCoeffs, headSpeed), apertureError(apertureCoeffs, aperture), temperatureError(temperatureCoeffs, temp))
        if costNew < cost and errorNew < tolerance:
            cost = costNew
            error = errorNew
        elif costNew < cost and errorNew > tolerance:
            aperture -= .01
            headSpeed -= .01
        elif costNew > cost and errorNew < tolerance:
            aperture += .01
            headSpeed += .01
        else:
            return(aperture, headSpeed)
        n += 1
         
minimize(inputs(), coefficients())

#residualStDev(dictionary('project2Speed.txt'), 'linear', regression(dictionary('project2Speed.txt'), 'linear')[0], regression(dictionary('project2Speed.txt'), 'linear')[1])