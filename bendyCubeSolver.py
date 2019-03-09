import copy


def createCubes(input):
    cubeArray = []
    for item in input:
        if item == 0:
            cubeArray.append(cube(True, (0, 0, 0)))
        elif item == 1:
            cubeArray.append(cube(False, (0, 0, 0)))

    return cubeArray


def solveCube(cubeArray):
    startingSolution = solution([], cubeArray, set())
    solutionQueue = []
    solutionQueue.append(startingSolution)
    solutions = []
    while len(solutionQueue) != 0:
        workingSolution = solutionQueue.pop(0)
        newSolutions = workingSolution.addNext()
        if newSolutions == None or len(newSolutions) == 0:
            if workingSolution.isComplete():
                solutions.append(workingSolution.workingSolution)
            continue
        for item in newSolutions:
            if item.isComplete():
                solutions.append(item.workingSolution)
            elif item.isValid():
                solutionQueue.append(item)
    return solutions


class cube:
    def __init__(self, isStraight, location):
        self.isStraight = isStraight
        self.location = location
        self.direction = "RIGHT"


class solution:
    def __init__(self, workingSolution, remainingCubes, taken):
        newCubes = []
        newRemainings = []
        for item in workingSolution:
            newCube = cube(
                item.isStraight, (item.location[0], item.location[1], item.location[2]))
            newCubes.append(newCube)
        for item in remainingCubes:
            newRemaining = cube(
                item.isStraight, (item.location[0], item.location[1], item.location[2]))
            newRemainings.append(newRemaining)
        self.workingSolution = newCubes
        self.remainingCubes = newRemainings
        self.taken = set(taken)

    def getBoundaries(self):
        maxX = 0
        minX = 0
        maxY = 0
        minY = 0
        maxZ = 0
        minZ = 0
        for cube in self.workingSolution:
            x, y, z = cube.location
            maxX = max(x, maxX)
            minX = min(x, minX)
            maxY = max(y, maxY)
            minY = min(y, minY)
            maxZ = max(z, maxZ)
            minZ = min(z, minZ)
        return [maxX, minX, maxY, minY, maxZ, minZ]

    def isValid(self):
        boundaries = self.getBoundaries()
        if abs(boundaries[0] - boundaries[1]) > 2 or abs(boundaries[2] - boundaries[3]) > 2 or abs(boundaries[4] - boundaries[5]) > 2:
            return False
        return True

    def addNext(self):
        if len(self.remainingCubes) == 0:
            return None
        if len(self.workingSolution) == 0:
            newCube = self.remainingCubes.pop(0)
            newCube.location = (0, 0, 0)
            self.taken.add(newCube.location)
            newCube.direction = "RIGHT"
            self.workingSolution.append(newCube)
            return [self]
        newCube = self.remainingCubes.pop(0)
        lastCube = self.workingSolution[len(self.workingSolution) - 1]
        if (lastCube.isStraight):
            x, y, z = lastCube.location
            direction = directions[lastCube.direction]
            x += direction[0]
            y += direction[1]
            z += direction[2]
            newCube.location = (x, y, z)
            if newCube.location in self.taken:
                return
            self.taken.add(newCube.location)
            newCube.direction = lastCube.direction
            self.workingSolution.append(newCube)
            return [self]
        else:
            direction = newDirections[lastCube.direction]
            toRet = []
            for dire in direction:
                newCubeCopy = cube(newCube.isStraight, newCube.location)
                x, y, z = lastCube.location
                direct = directions[dire]
                x += direct[0]
                y += direct[1]
                z += direct[2]
                newCubeCopy.location = (x, y, z)
                if newCubeCopy.location in self.taken:
                    continue
                else:
                    taken = set(self.taken)
                    taken.add(newCubeCopy.location)
                    newCubeCopy.direction = dire
                    newSolution = solution(
                        self.workingSolution, self.remainingCubes, taken)
                    newSolution.workingSolution.append(newCubeCopy)
                    toRet.append(newSolution)

            return toRet

    def isComplete(self):
        return self.isValid() and len(self.remainingCubes) == 0


directions = {"UP": (0, 1, 0), "DOWN": (0, -1, 0), "LEFT": (-1, 0, 0),
              "RIGHT": (1, 0, 0), "FORWARD": (0, 0, 1), "BACKWARD": (0, 0, -1)}
newDirections = {"RIGHT": ["UP", "FORWARD", "DOWN", "BACKWARD"], "LEFT": ["UP", "FORWARD", "DOWN", "BACKWARD"], "UP": ["LEFT", "RIGHT", "FORWARD", "BACKWARD"], "DOWN": [
    "LEFT", "RIGHT", "FORWARD", "BACKWARD"], "FORWARD": ["UP", "DOWN", "LEFT", "RIGHT"], "BACKWARD": ["UP", "DOWN", "LEFT", "RIGHT"]}

x = [0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0,
     1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0]
cubeArray = createCubes(x)
answer = solveCube(cubeArray)
for item in answer:
    print("SOLUTION")
    for thing in item:
        print(thing.location)
