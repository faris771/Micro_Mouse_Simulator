from constants import *
from Algorithms.Algorithm import Algorithm
import API


class FloodFill(Algorithm):

    def execute(self):
        API.log("FLOODFILL RUNNING...")


        # Mouse Orientation: 0 > up | 1 > right | 2 > down | 3 > left |
        orientation = 0
        # Current mouse Position, the starting point being 0, 0
        current_position = [0, 0]
        # saves information about nodes that it passed
        # and nodes that it had to make a decision
        nodesSinceLastDecision = []  # stack
        lastDecisionNode = []

        while MAZE_SETTINGS[current_position[0]][current_position[1]] != 0:
            for i in range(16):
                for j in range(16):
                    API.setText(i, j, str(MAZE_SETTINGS[i][j]))
            API.setColor(current_position[1],current_position[0],'B')

            row, col = current_position
            F = API.wallFront()
            R = API.wallRight()
            L = API.wallLeft()

            # Forward, Right, Left nodes
            nodesAround = [(), (), ()]
            valuesAround = [float("inf"), float("inf"), float("inf")] # around blocks that can be visited

            if not F:
                # no wall in front
                if orientation == 0:
                    frontVal = MAZE_SETTINGS[row + 1][col]
                    nodesAround[0] = (row + 1, col)
                elif orientation == 1:
                    frontVal = MAZE_SETTINGS[row][col + 1]
                    nodesAround[0] = (row, col + 1)
                elif orientation == 2:
                    frontVal = MAZE_SETTINGS[row - 1][col]
                    nodesAround[0] = (row - 1, col)
                elif orientation == 3:
                    frontVal = MAZE_SETTINGS[row][col - 1]
                    nodesAround[0] = (row, col - 1)
                valuesAround[0] = frontVal

            if not R:
                # no wall in the right
                if orientation == 0:
                    rightVal = MAZE_SETTINGS[row][col + 1]
                    nodesAround[1] = (row, col + 1)
                elif orientation == 1:
                    rightVal = MAZE_SETTINGS[row - 1][col]
                    nodesAround[1] = (row - 1, col)
                elif orientation == 2:
                    rightVal = MAZE_SETTINGS[row][col - 1]
                    nodesAround[1] = (row, col - 1)
                elif orientation == 3:
                    rightVal = MAZE_SETTINGS[row + 1][col]
                    nodesAround[1] = (row + 1, col)
                valuesAround[1] = rightVal

            if not L:
                # no wall in the left
                if orientation == 0:
                    leftVal = MAZE_SETTINGS[row][col - 1]
                    nodesAround[2] = (row, col - 1)
                if orientation == 1:
                    leftVal = MAZE_SETTINGS[row + 1][col]
                    nodesAround[2] = (row + 1, col)
                if orientation == 2:
                    leftVal = MAZE_SETTINGS[row][col + 1]
                    nodesAround[2] = (row, col + 1)
                if orientation == 3:
                    leftVal = MAZE_SETTINGS[row - 1][col]
                    nodesAround[2] = (row - 1, col)
                valuesAround[2] = leftVal


            # simple flood fill to nodes the mouse passed lastly
            if lastDecisionNode and (row, col) in lastDecisionNode: # visited
                prev = (row, col)
                for node in nodesSinceLastDecision[-2]: # top of stack
                    MAZE_SETTINGS[node[0]][node[1]] = MAZE_SETTINGS[prev[0]][prev[1]] + 1 # cost + 1
                    prev = (node[0], node[1])

            if L and R and F:
                # Dead End, we need to turn 180 degrees
                API.turnRight()
                API.turnRight()
                API.moveForward()
                for nodesSince in nodesSinceLastDecision: # push move to stack
                    nodesSince.append((row, col))

                # updating position and orientation based on orientation
                if orientation == 0:
                    current_position[0] -= 1
                    orientation = 2
                elif orientation == 1:
                    current_position[1] -= 1
                    orientation = 3
                elif orientation == 2:
                    current_position[0] += 1
                    orientation = 0
                elif orientation == 3:
                    current_position[1] += 1
                    orientation = 1
                continue

            lowerNeighbor = min(valuesAround)

            if lowerNeighbor == valuesAround[0]:
                # lowerNeighbor is Front
                API.moveForward()
                for nodesSince in nodesSinceLastDecision:
                    nodesSince.append((row, col))

                # updating position based on orientation
                if orientation == 0:
                    current_position[0] += 1
                elif orientation == 1:
                    current_position[1] += 1
                elif orientation == 2:
                    current_position[0] -= 1
                elif orientation == 3:
                    current_position[1] -= 1


            elif lowerNeighbor == valuesAround[1]: # if least value is Right of mouse
                # lowerNeighbor is Right side
                API.turnRight()
                API.moveForward()
                for nodesSince in nodesSinceLastDecision:
                    nodesSince.append((row, col))

                # updating position and orientation based on orientation
                if orientation == 0:
                    current_position[1] += 1
                    orientation = 1

                elif orientation == 1:
                    current_position[0] -= 1
                    orientation = 2

                elif orientation == 2:
                    current_position[1] -= 1
                    orientation = 3

                elif orientation == 3:
                    current_position[0] += 1
                    orientation = 0

            elif lowerNeighbor == valuesAround[2]:
                # lowerNeighbor is Left side
                API.turnLeft()
                API.moveForward()
                for nodesSince in nodesSinceLastDecision:
                    nodesSince.append((row, col))

                # updating position and orientation based on orientation
                if orientation == 0:
                    current_position[1] -= 1
                    orientation = 3

                elif orientation == 1:
                    current_position[0] += 1
                    orientation = 0

                elif orientation == 2:
                    current_position[1] += 1
                    orientation = 1

                elif orientation == 3:
                    current_position[0] -= 1
                    orientation = 2

            if (not L and not R) or (not L and not F) or (not F and not R): # cross road
                # mouse is making a new decision, so we update our arrays to reflect that
                nodesSinceLastDecision.append([])
                # API.log(nodesSinceLastDecision)
                if (row, col) not in lastDecisionNode: # if we haven't visited this node before
                    lastDecisionNode.append((row, col))


        API.log("FINISHED!!")
