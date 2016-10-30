from math import exp, log
from statistics import stdev

def dictionary(file):

    dict = {}
    
    with open(file) as data:
    
        for line in data:
        
            try:
        
                x = float(line.split()[0])
                y = float(line.split()[1])
                
                if y == 0:
                
                    y = .000001
                    
                dict[x] = y
            
            # removes words from input data
            except:
                pass
            
    #close file
    
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
            residList.append(log(y) - log(yPrediction)) 
            
        elif type == 'power':
        
            yPrediction = exp(a0) * (x ** a1)
            residList.append(log(y) - log(yPrediction)) 
            
    stDev = stdev(residList)
    
    return(stDev)

def regression(dict, type):
    # figure out the linear regression
    n = 0
    sumx = 0
    sumy = 0
    sumxy = 0
    sumx2 = 0
    
    offset = maxOffset(dict)
    
    for item in dict:
    
        if type == 'linear':
        
            x = item + offset
            y = dict[item]     
            
        elif type == 'exponential':
        
            try:
            
                x = item + offset
                y = log(dict[item])
                
            except ValueError:
                
                y = log(.0000000001)
                
        elif type == 'power':
            
            try:
            
                x = log(item) + offset
                y = log(dict[item])
                
            except ValueError:
            
                x = log(.0000000001)
                y = log(.0000000001)
            
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
                
            if abs(log(y) - log(yPrediction)) < 2 * stDev:
            
                cleanDataDict[x] = y
                
            else:
                
                dirtyData[x] = y
   
        elif type == "power":
        
            yPrediction = exp(a0) * (x ** a1)
            
            if abs(log(y) - log(yPrediction)) < 2 * stDev:
            
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
    tolerance = float(input("Enter print tolerance in millimeters: "))
    
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

def gradErrorFunc(coefficients, aperture, temp):

    a0 = coefficients[0]
    a1 = coefficients[1]
    a2 = coefficients[2]
    a3 = coefficients[3]
    a4 = coefficients[4]
    a5 = coefficients[5]
    
    gradient = [a1, a3 * exp(a2 + a3 * aperture), a5 * exp(a4) * temp ** (a5 - 1)]
    return(gradient)
    
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

def gradCostFunc(temp, volume, aperture, headSpeed):

    if printingTime  >= cureTime:
        grad = [-18 * volume / ((headSpeed ** 2) * aperture), -18 * volume / (headSpeed * (aperture ** 2)), 0]
    else:
        grad = [-18 * 1570 / temp ** 2 , 0, 0]
    return(grad)
    
def lagrangeMultiplier(gradF, gradG, tolerance, headSpeed, aperture, temp):
    pass

def minimize(constraint, coefficients):

    volume = constraint[0]
    tolerance = constraint[1]
    speedCoeffs = coefficients[0:2]
    apertureCoeffs = coefficients[2:4]
    temperatureCoeffs = coefficients[4:6]
    
    errorNew = 0
    tempOptimized = 0
    apertureOptimized = 0
    speedOptimized = 0

    temp = 36
    aperture = 4
    headSpeed = 5
    
    cost = 10000000000000
    
    apertureVals = range(1, 20)
    tempVals = range(40, 360)
    speedVals = range(1, 30)
    
    print("Phase 1 optimization in progress...")
    
    for aperture in apertureVals:

        aperture = aperture / 10
        #print(aperture, "...")
        for headSpeed in speedVals:
        
            headSpeed = headSpeed / 10
            
            for temp in tempVals: 
            
                temp = temp / 10
                
                costNew = costFunc(volume, productionTime(printTime(volume, headSpeed, aperture), cureTime(temp)))
                error = errorFunc(speedError(speedCoeffs, headSpeed), apertureError(apertureCoeffs, aperture), temperatureError(temperatureCoeffs, temp))
                
                if costNew < cost and error < tolerance:
                
                    cost = costNew
                    errorNew = error
                    apertureOptimized = aperture
                    tempOptimized = temp
                    speedOptimized = headSpeed
                    
    if cost == 10000000000000 and error > tolerance:
    
        apertureVals = range(1, 20)
        tempVals = range(400, 3600)
        speedVals = range(1, 30)
        
    
    else:
    
        minAperture = int(100 * apertureOptimized) - 10
        if minAperture <= 0:
            minAperture = 1
        maxAperture = int(100 *apertureOptimized) + 10
    
        minTemp = int(100 * tempOptimized) - 10
        maxTemp = int(100 * tempOptimized) + 10
    
        minSpeed = int(100 * speedOptimized) - 10
        if minSpeed <= 0:
            minSpeed = 1
        maxSpeed = int(100 * speedOptimized) + 10
    
        apertureVals  = range(minAperture, maxAperture)
        tempVals = range(minTemp, maxTemp)
        speedVals = range(minSpeed, maxSpeed)
    
    print("Phase 2 optimization in progress...")
    
    for aperture in apertureVals:
         
        aperture = aperture / 100
        #print(aperture)
        for headSpeed in speedVals:
        
            headSpeed = headSpeed / 100
            #print(headSpeed)
            for temp in tempVals: 
            
                temp = temp / 100
                #print(temp)
                costNew = costFunc(volume, productionTime(printTime(volume, headSpeed, aperture), cureTime(temp)))
                error = errorFunc(speedError(speedCoeffs, headSpeed), apertureError(apertureCoeffs, aperture), temperatureError(temperatureCoeffs, temp))
                #print(costNew, error)
                if costNew < cost and error < tolerance:
                    #print("yay")
                    cost = costNew
                    errorNew = error
                    apertureOptimized = aperture
                    tempOptimized = temp
                    speedOptimized = headSpeed
                    
    if cost == 10000000000000 and error > tolerance:
    
        apertureVals = range(1, 20)
        tempVals = range(4000, 5000)
        speedVals = range(1, 30)
        
    else:
    
        minAperture = int(1000 * apertureOptimized) - 100
        if minAperture <= 0:
            minAperture = 1
        maxAperture = int(1000 *apertureOptimized) + 100
    
        minTemp = int(1000 * tempOptimized) - 100
        maxTemp = int(1000 * tempOptimized) + 100
    
        minSpeed = int(1000 * speedOptimized) - 100
        if minSpeed <= 0:
            minSpeed = 1
        maxSpeed = int(1000 * speedOptimized) + 100
    
        apertureVals  = range(minAperture, maxAperture)
        tempVals = range(minTemp, maxTemp)
        speedVals = range(minSpeed, maxSpeed)
    
    print("Final optimization in progress...")

    for aperture in apertureVals:
        
        aperture = aperture / 1000
        
        for headSpeed in speedVals:
        
            headSpeed = headSpeed / 1000
            
            for temp in tempVals: 
            
                temp = temp / 1000
                
                costNew = costFunc(volume, productionTime(printTime(volume, headSpeed, aperture), cureTime(temp)))
                error = errorFunc(speedError(speedCoeffs, headSpeed), apertureError(apertureCoeffs, aperture), temperatureError(temperatureCoeffs, temp))
                
                if costNew < cost and error < tolerance:
                    #print("valid")
                    cost = costNew
                    errorNew = error
                    apertureOptimized = aperture
                    tempOptimized = temp
                    speedOptimized = headSpeed 
     
    if cost == 10000000000000 and error > tolerance:
        return("Error: tolerance could not be reached.")
        
    else:
        return("The part will cost $%.2f with an error of plus or minus %.2f mm. Print at %.3f degrees Celsius, with an aperture of %.3f mm and a speed of %.3f cm/s. \nPrint time will be %.3f minutes." 
            % (cost, errorNew, tempOptimized, apertureOptimized, speedOptimized, productionTime(printTime(volume, speedOptimized, apertureOptimized), cureTime(tempOptimized))))
    
print(minimize(inputs(), coefficients()))

#residualStDev(dictionary('project2Speed.txt'), 'linear', regression(dictionary('project2Speed.txt'), 'linear')[0], regression(dictionary('project2Speed.txt'), 'linear')[1])