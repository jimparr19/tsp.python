# function for simple tsp problem

from math import sqrt
import matplotlib
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
    matplotlib.pyplot.plot(x, y, 'o', markerfacecolor='green', markersize=10)
    matplotlib.pyplot.hold(True)
    matplotlib.pyplot.axis('equal')
    matplotlib.pyplot.axis('off')
    xr = []
    yr = []
    for j in cityOrder:
        xr.append(x[j])
        yr.append(y[j])
    matplotlib.pyplot.plot(xr, yr, '-', color=(0.1, 0.1, 0.1, 1))


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


def reverseSections(cityOrder):
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


def objectiveFunction(matrix, cityOrder):
    '''Objective function to minimize'''
    return routeLength(matrix, cityOrder)


def hillClimb(initialRoute, matrix, maxEvaluations):
    '''Hillclim given move operator reverseSections'''
    bestSolution = initialRoute
    bestScore = objectiveFunction(matrix, bestSolution)
    iEvaluation = 1
    while iEvaluation < maxEvaluations:
        # examine moves around our current position
        moveMade = False
        for next in reverseSections(bestSolution):
            if iEvaluation >= maxEvaluations:
                break
            # see if this move is better than the current
            nextScore = objectiveFunction(matrix, next)
            iEvaluation += 1
            if nextScore < bestScore:
                bestSolution = next
                bestScore = nextScore
                moveMade = True
                break  # depth first search
            if not moveMade:
                break  # we couldn't find a better move

    return (iEvaluation, bestScore, bestSolution)


def test_routeLength():
    coords = importCoordsFromFile('city100.txt')
    distanceMatrix = createDistanceMatrix(coords)
    initialGuess = initialRoute(len(coords))
    [totalEvaluations, score, solution] = hillClimb(initialGuess,
                                                    distanceMatrix, 50000)
    visualiseRoute(coords, solution)
