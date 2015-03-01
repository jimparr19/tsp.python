# function for simple tsp problem

from math import sqrt
import pylab
import random

def importCoordsFromFile(fileName):
    '''Import coords from txt file'''
    file = open(fileName, 'r')
    coords = []
    for line in file:
        x, y = line.strip().split(',')
        coords.append((float(x), float(y)))
    return coords


def createDistanceMatrix(coords):
    '''Create a distance matrix given coords based on straight line distance'''
    matrix = {}
    for i, (x1, y1) in enumerate(coords):
        for j, (x2, y2) in enumerate(coords):
            dx, dy = x1-x2, y1-y2
            dist = sqrt(dx*dx + dy*dy)
            matrix[i, j] = dist
    return matrix


def routeLength(matrix, cityOrder):
    '''Length of route based on the distance matrix and the city order'''
    total = 0
    numberOfCities = len(cityOrder)
    for i in range(numberOfCities):
        j = (i+1) % numberOfCities
        iCity = cityOrder[i]
        jCity = cityOrder[j]
        total += matrix[iCity, jCity]
    return total


def visualiseRoute(coords, cityOrder):
    '''Visualise all cities and the route taken'''
    x = []
    y = []
    for i, (x1, y1) in enumerate(coords):
        x.append(x1)
        y.append(y1)
    pylab.plot(x, y, '-o', markerfacecolor='green', markersize=10,
               color=(0.5, 0.5, 0.5, 1))


def initialRoute(numberOfCities):
    '''Randomise an initial route'''
    cityOrder = range(numberOfCities)
    random.shuffle(cityOrder)
    return cityOrder


def allPairs(size):
    '''Generator for all i,j pairs for i,j from 0-size'''
    r1 = range(size)
    r2 = range(size)
    random.shuffle(r1)
    random.shuffle(r2)
    for i in r1:
        for j in r2:
            yield (i, j)
        

def reversSections(cityOrder):
    '''Generator for to reverse all pairs'''
    for i, j in allPairs(len(cityOrder)):
        if i != j:
            copy = cityOrder[:]
            if i < j:
                copy[i:j+1] = reversed(cityOrder[i:j+1])
            else:
                copy[i+1:] = reversed(cityOrder[:j])
                copy[:j] = reversed(cityOrder[i+1:])
            if copy != cityOrder:
                yield copy

#    def test_routeLength():
#        coords = importCoordsFromFile('city100.txt')
#        distanceMatrix = createDistanceMatrix(coords)
#        cityOrder = range(100)
#        routeLength = totalRouteLength(distanceMatric, routeOrder)