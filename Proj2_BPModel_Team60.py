# Project 2 BioPrinter Model
# File: proj2_BPModel_team60.py
# Date: 1 November 2016
# By: Naveed Riaziat
# nriaziat
# Logan Walters
# walte123
# Corey Hellman
# chellma
# Ian Bernander
# ibernand
# Section: 4
# Team: 60
#
# ELECTRONIC SIGNATURE
# Naveed Riaziat
# Logan Walters
# Corey Hellman
# Ian Bernanders
#
# The electronic signatures above indicate that the program
# submitted for evaluation is the combined effort of all
# team members and that each member of the team was an
# equal participant in its creation. In addition, each
# member of the team has a general understanding of
# all aspects of the program development and execution.
#
# minimizes bioprinting cost based on a given tolerance and volume
#parameters are defined from error data files

from math import exp, log
from statistics import stdev

# adds the input data to a dictionary
def dictionary(file):
    # create an empty dictionary to store input data
    dict = {}
    
    with open(file) as data:
    
        for line in data:
        
            try:
                
                x = float(line.split()[0])
                y = float(line.split()[1])
                
                # sets small y values to nearly 0 to allow logarithm
                if y == 0:
                
                    y = .000001
                    
                dict[x] = y
            
            # removes words from input data
            except:
                pass
            
    #close file
    
    return(dict)

# finds the x offset of the minimum data value from 0
def maxOffset(dict):

	offset = 0
    
	for item in dict:
        # for negative items in the dictionary, find the largest one
		if item < 0:
        
			if abs(item) > offset:
            
				offset = abs(item)
                
	return(offset)

# finds the standard deviation of the residuals    
def residualStDev(dict, type, a0, a1):

    residList = []
    
    for item in dict:
        x = item
        y = dict[item]
        
        if type == 'linear':
            # predicts y value with linear regression
            yPrediction = a0 + (a1 * x)
            residList.append(y - yPrediction) 
            
        elif type == 'exponential':
            # predicts y value with exponential regression 
            yPrediction = exp(a0 + (a1 * x))
            residList.append(log(y) - log(yPrediction)) 
            
        elif type == 'power':
            # predicts y value with power regression
            yPrediction = exp(a0) * (x ** a1)
            residList.append(log(y) - log(yPrediction)) 
            
    stDev = stdev(residList)
    
    return(stDev)

# creates a regression line based on the input data type
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
            # move x values right to account for offset
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
            
            # prevents logarithm issues from x = 0 
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
 
 # removes noisy data from the input
def cleaner(dict, type, coeff):

    a0 = coeff[0]
    a1 = coeff[1]
    
    cleanDataDict = {}
    
    stDev = residualStDev(dict, type, a0, a1)
    xOffset = maxOffset(dict)
    
    for item in dict:
    
        x = item + xOffset
        y = dict[item]
        
        if type == "linear":
        
            yPrediction = a0 + (a1 * x)
            
            # checks points vs residual standard deviation
            if abs(y - yPrediction) < 2 * stDev:
            
                cleanDataDict[x] = y
                
                
        elif type == "exponential":
        
            yPrediction = exp(a0 + (a1 * x))
            
            # checks points vs residual standard deviation
            if abs(log(y) - log(yPrediction)) < 2 * stDev:
            
                cleanDataDict[x] = y
                

   
        elif type == "power":
        
            yPrediction = exp(a0) * (x ** a1)
            
            # checks points vs residual standard deviation
            if abs(log(y) - log(yPrediction)) < 2 * stDev:
            
                cleanDataDict[x] = y

    return(cleanDataDict)
  
# organizes initial data  
def dataHandling(file, regType):

    data = dictionary(file)
    initialReg = regression(data, regType)
    initA0 = initialReg[0]
    initialA1 = initialReg[1]
    cleanData = cleaner(data, regType, initialReg)
    finalReg = regression(cleanData, regType)
    
    return(finalReg)
 
# stores the regression coefficients for each regression 
def coefficients():

    speedCoeffs = dataHandling('project2Speed.txt','linear')
    apertureCoeffs = dataHandling('project2Aperture.txt', 'exponential')
    temperatureCoeffs = dataHandling('project2Temperature.txt', 'power')
    print(speedCoeffs,apertureCoeffs,temperatureCoeffs)

    return(speedCoeffs[0], speedCoeffs[1], apertureCoeffs[0], apertureCoeffs[1],
        temperatureCoeffs[0], temperatureCoeffs[1])

# takes user inputs for tolerance and volume
def inputs():

    bedSize = 10000
    volume = 'None'
    tolerance = 'None'
    
    # as long as a valid volume is not inputted
    while volume == 'None':
    
        try:    
            
            volume = float(input("Enter print volume in cubic centimeters: "))
            
            # if the inputted volume is greater than the volume of the printer
            if volume >= bedSize:
            
                confirmation = input('Warning: This volume may not fit on the print bed. Use this value? (Y/N)\n').lower()
                
                if confirmation != 'y':
                    volume = 'None'
             
             # ensures positive volumes
            elif volume <= 0:
                print("Volumes must be greater than 0.")
                volume = 'None'
                
        # makes sure volume is a number       
        except ValueError:
        
            print("Invalid Volume.")
            volume = 'None'
           
    while tolerance == 'None':
    
        try:
        
            tolerance = float(input("Enter print tolerance in millimeters: "))
            
            # ensures tolerance is greater than 0
            if tolerance <= 0:
            
                tolerance = 'None'
                
                print("Tolerance must be greater than 0.")             
       
        # ensures tolerance is a number
        except ValueError:
        
            tolerance = 'None'
            print("Invalid tolerance.")
            
    return(volume, tolerance)
    
# determines error from speed given the regression and speed  
def speedError(coefficients, headSpeed):
        
    a0 = coefficients[0]
    a1 = coefficients[1]
    
    speedError = a1 * headSpeed 
    
    return(speedError)

# determines the aperture error based on regression and aperture    
def apertureError(coefficients, aperture):

    a0 = coefficients[0]
    a1 = coefficients[1]
    
    apertureError = exp(a0 + (a1 * aperture))
    
    return(apertureError)

# determines temperature error based on regression and temp
def temperatureError(coefficients, temp):

    a0 = coefficients[0]
    a1 = coefficients[1]
    
    temperatureError = exp(a0) * temp ** a1
    
    return(temperatureError)
    
# determines the total dimensional error
def errorFunc(speedError, apertureError, temperatureError):

    error = speedError + apertureError + temperatureError
    
    return(error)

# determines print time in minutes
def printTime(volume, headSpeed, aperture):
    
    volume = volume * 1000 #convert cm3 to mm3

    printingTime = volume / (headSpeed * aperture)
    
    printingTime = printingTime / 60 #convert seconds to minutes
    
    return(printingTime)

# determines cure time based on temperature    
def cureTime(temp):
 
    cureTime = 1570 / temp + 20 
               
    return(cureTime)

# determines production time based on cure and print time
def productionTime(printingTime, cureTime):

    if printingTime >= cureTime:
    
        prodTime = printingTime + 20
        
    elif printingTime < cureTime:
    
        prodTime = cureTime
        
    return(prodTime)
 
# finds the cost pased on volume and production time 
def costFunc(volume, productionTime):

    c = 500 * volume + 18 * productionTime
    
    return(c)

# minimizes the cost using and optimized brute force method
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
    
    # large cost to determine if no solutions could be found
    cost = 1.7976931348623157e+308
    
    apertureVals = range(1, 20)
    tempVals = range(40, 360)
    speedVals = range(1, 30)
    
    print("Phase 1 optimization in progress...")
    
    # searches for all values in given ranges to .1 tolerance
    for aperture in apertureVals:

        aperture = aperture / 10
        
        for headSpeed in speedVals:
        
            headSpeed = headSpeed / 10
            
            for temp in tempVals: 
            
                temp = temp / 10
                
                # evaluates the functions with all given values
                costNew = costFunc(volume, productionTime(printTime(volume,
                                headSpeed, aperture), cureTime(temp)))
                error = errorFunc(speedError(speedCoeffs, headSpeed), 
                                apertureError(apertureCoeffs, aperture), 
                                temperatureError(temperatureCoeffs, temp))
                
                # stores values if cost is lower than previous low cost 
                #and error is acceptable
                if costNew < cost and error < tolerance:
                
                    cost = costNew
                    errorNew = error
                    apertureOptimized = aperture
                    tempOptimized = temp
                    speedOptimized = headSpeed

                # stores values with lower tolerance for equivalent cost    
                elif costNew <= cost and error < errorNew:
                    
                    cost = costNew
                    errorNew = error
                    apertureOptimized = aperture
                    tempOptimized = temp
                    speedOptimized = headSpeed
                    
    # if no solution was found, try entire range again               
    if cost == 1.7976931348623157e+308 and error > tolerance:
    
        apertureVals = range(1, 20)
        tempVals = range(400, 3600)
        speedVals = range(1, 30)
        
    # searches a smaller range of values localized around previous solution
    else:
        
        minAperture = int(100 * apertureOptimized) - 20
        if minAperture <= 0:
            minAperture = 1
        maxAperture = int(100 *apertureOptimized) + 20
        if maxAperture > 191:
            maxAperture = 191
    
        minTemp = int(100 * tempOptimized) - 20
        if minTemp < 401:
            minTemp = 401
        maxTemp = int(100 * tempOptimized) + 20
        if maxTemp > 3601:
            maxTemp = 3601
            
        minSpeed = int(100 * speedOptimized) - 20
        if minSpeed <= 0:
            minSpeed = 1
        maxSpeed = int(100 * speedOptimized) + 20
        if maxSpeed > 301:
            maxSpeed = 301
    
        apertureVals  = range(minAperture, maxAperture)
        tempVals = range(minTemp, maxTemp)
        speedVals = range(minSpeed, maxSpeed)
    
    print("Phase 2 optimization in progress...")
    
    # checks all parameter values in new range
    for aperture in apertureVals:
         
        aperture = aperture / 100
        
        for headSpeed in speedVals:
        
            headSpeed = headSpeed / 100
            
            for temp in tempVals: 
            
                temp = temp / 100
                
                costNew = costFunc(volume, productionTime(printTime(volume,
                                headSpeed, aperture), cureTime(temp)))
                error = errorFunc(speedError(speedCoeffs, headSpeed), 
                                apertureError(apertureCoeffs, aperture), 
                                temperatureError(temperatureCoeffs, temp))

                if costNew < cost and error < tolerance:
                    cost = costNew
                    errorNew = error
                    apertureOptimized = aperture
                    tempOptimized = temp
                    speedOptimized = headSpeed
                
                elif costNew <= cost and error < errorNew:
                    
                    cost = costNew
                    errorNew = error
                    apertureOptimized = aperture
                    tempOptimized = temp
                    speedOptimized = headSpeed
                    
    if cost == 1.7976931348623157e+308 and error > tolerance:
    
        apertureVals = range(1, 20)
        tempVals = range(4000, 5000)
        speedVals = range(1, 30)
        
    else:
    
        minAperture = int(1000 * apertureOptimized) - 20
        if minAperture <= 0:
            minAperture = 1
        maxAperture = int(1000 *apertureOptimized) + 20
        if maxAperture > 1901:
            maxAperture = 1901
    
        minTemp = int(1000 * tempOptimized) - 20
        if minTemp < 4001:
            minTemp = 4001
        maxTemp = int(1000 * tempOptimized) + 20
        if maxTemp > 36001:
            maxTemp = 36001
    
        minSpeed = int(1000 * speedOptimized) - 20
        if minSpeed <= 0:
            minSpeed = 1
        maxSpeed = int(1000 * speedOptimized) + 20
        if maxSpeed > 3001:
            maxSpeed = 3001
        
        
        apertureVals  = range(minAperture, maxAperture)
        tempVals = range(minTemp, maxTemp)
        speedVals = range(minSpeed, maxSpeed)

    print("Final optimization in progress...")
    
    # checks all values for .001 tolerance
    for aperture in apertureVals:
        
        aperture = aperture / 1000
        
        for headSpeed in speedVals:
        
            headSpeed = headSpeed / 1000
            
            for temp in tempVals: 
            
                temp = temp / 1000
                
                costNew = costFunc(volume, productionTime(printTime(volume, 
                                headSpeed, aperture), cureTime(temp)))
                error = errorFunc(speedError(speedCoeffs, headSpeed), 
                                apertureError(apertureCoeffs, aperture), 
                                temperatureError(temperatureCoeffs, temp))
                
                if costNew < cost and error < tolerance:
                    #print("valid")
                    
                    cost = costNew
                    errorNew = error
                    apertureOptimized = aperture
                    tempOptimized = temp
                    speedOptimized = headSpeed 
                    
                elif costNew <= cost and error < errorNew:
                    
                    cost = costNew
                    errorNew = error
                    apertureOptimized = aperture
                    tempOptimized = temp
                    speedOptimized = headSpeed 
                    
    if cost == 1.7976931348623157e+308 and error > tolerance:
        return("Error: tolerance could not be reached.")
        
    else:
        
        return(cost, errorNew, tempOptimized, apertureOptimized, 
                    speedOptimized, printTime, volume, speedCoeffs, apertureCoeffs,
                    temperatureCoeffs)

def variability(dataList):
        
        # makes sure data is being input, and not an error from the last fxns
        if type(dataList) != tuple:
            return(dataList)
            
        cost = dataList[0]
        errorNew = dataList[1]
        tempOptimized = dataList[2]
        apertureOptimized = dataList[3]
        speedOptimized = dataList[4]
        volume = dataList[6]
        speedCoeffs  = dataList[7]
        apertureCoeffs = dataList[8]
        temperatureCoeffs = dataList[9]
        
        # calculates production time for given data
        prodTime = productionTime(printTime(volume, speedOptimized, 
                        apertureOptimized), cureTime(tempOptimized))
        
        # changes data down by half of our precision 
        tempOptimized -= .0005
        speedOptimized -= .0005
        apertureOptimized -= .0005

        # recalculates time, cost, error
        timeMin = productionTime(printTime(volume, speedOptimized, 
                        apertureOptimized), cureTime(tempOptimized))
        costMin = costFunc(volume, timeMin)
        errorMin = errorFunc(speedError(speedCoeffs, speedOptimized), 
                        apertureError(apertureCoeffs, apertureOptimized), 
                        temperatureError(temperatureCoeffs, tempOptimized))
         
        #changes data up by half our precision
        tempOptimized += .001
        speedOptimized += .001
        apertureOptimized += .001
        
        # recalculates time, cost, and error
        timeMax = productionTime(printTime(volume, speedOptimized,
                        apertureOptimized), cureTime(tempOptimized))
        costMax = costFunc(volume, timeMax)
        errorMax = errorFunc(speedError(speedCoeffs, speedOptimized), 
                        apertureError(apertureCoeffs, apertureOptimized), 
                        temperatureError(temperatureCoeffs, tempOptimized))
            
        
        return('Speed: %.3f mm/s\n'
               'Aperture: %.3f mm^2\n'
               'Temperature: %.2f degrees Celsius\n'
               'Cost: $%.2f (Expected Range: $%.2f to $%.2f)\n'
               'Dimensional Error: %.3f mm (Expected Range: %.3f mm to '
                                        '%.3f mm)\n'
               'Production Time: %.3f minutes (Expected Range: %.3f '
                                        'minutes to %.3f minutes'
               % (speedOptimized - .0005, apertureOptimized - .0005, 
                    tempOptimized - .0005, cost, costMax, costMin, errorNew,
                    errorMin, errorMax, prodTime, timeMax, timeMin))

print(variability(minimize(inputs(), coefficients())))
