from constants import *
from Algorithms.Algorithm import Algorithm
import API


class FloodFill(Algorithm):

    def execute(self):

        API.log("FLOODFILL RUNNING...")

        #  0 > up, 1 > right,  2 > down, 3 > left
        orientation = 0
        current_position = [0, 0]  # start point

        nodes_since_last_decision = []  # stack
        last_decision_node = []

        while MAZE_SETTINGS[current_position[0]][current_position[1]] != 0:

            self.update_maze_values()

            API.setColor(current_position[1], current_position[0], 'B')

            row, col = current_position
            front_wall = API.wallFront()
            right_wall = API.wallRight()
            left_wall = API.wallLeft()

            # Forward, Right, Left nodes
            neighbouring_nodes = [(), (), ()]
            neighbouring_values = [float("inf"), float("inf"), float("inf")]  # around blocks that can be visited

            self.check_walls_around(front_wall, left_wall, right_wall, col, neighbouring_nodes, orientation, row,
                                    neighbouring_values)

            # if we have visited this node before, we update the nodes we have visited since the last decision
            is_visited_node = last_decision_node and (row, col) in last_decision_node
            if is_visited_node:  # visited
                self.update_previously_visited_nodes(col, nodes_since_last_decision, row)

            dead_end = left_wall and right_wall and front_wall
            if dead_end:
                orientation = self.turn_back(col, current_position, nodes_since_last_decision, orientation, row)
                continue

            lowest_neighbor = min(neighbouring_values)
            orientation = self.choose_lowest_neigbour(col, current_position, lowest_neighbor, nodes_since_last_decision,
                                                      orientation, row, neighbouring_values)

            cross_road = (not left_wall and not right_wall) or (not left_wall and not front_wall) or (
                    not front_wall and not right_wall)

            if cross_road:
                # mouse is making a new decision, so we update our arrays to reflect that
                self.update_decision_nodes(col, last_decision_node, nodes_since_last_decision, row)

        API.log("FINISHED!!")

    def update_decision_nodes(self, col, last_decision_node, nodes_since_last_decision, row):
        nodes_since_last_decision.append([])
        # API.log(nodesSinceLastDecision)
        if (row, col) not in last_decision_node:  # if we haven't visited this node before
            last_decision_node.append((row, col))
            #

    def update_previously_visited_nodes(self, col, nodes_since_last_decision, row):
        previous_node = (row, col)
        for node in nodes_since_last_decision[-2]:  # top of stack
            MAZE_SETTINGS[node[0]][node[1]] = MAZE_SETTINGS[previous_node[0]][previous_node[1]] + 1  # cost + 1
            previous_node = (node[0], node[1])

    def choose_lowest_neigbour(self, col, current_position, lower_neighbor, nodes_since_last_decision, orientation, row,
                               neighbouring_nodes):
        if lower_neighbor == neighbouring_nodes[0]:
            # lowerNeighbor is Front
            API.moveForward()
            for nodesSince in nodes_since_last_decision:
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


        elif lower_neighbor == neighbouring_nodes[1]:  # if least value is Right of mouse
            # Right side
            API.turnRight()
            API.moveForward()
            for nodesSince in nodes_since_last_decision:
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

        elif lower_neighbor == neighbouring_nodes[2]:
            #  Left side
            API.turnLeft()
            API.moveForward()
            for nodesSince in nodes_since_last_decision:
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
        return orientation

    def turn_back(self, col, current_position, nodes_since_last_decision, orientation, row):
        API.turnRight()
        API.turnRight()
        API.moveForward()
        for nodesSince in nodes_since_last_decision:  # push move to stack
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
        return orientation

    def check_walls_around(self, front_wall, left_wall, right_wall, col, neighbouring_nodes, orientation, row, neighbouring_values):

        if not front_wall:
            # no wall in front
            if orientation == 0:
                front_val = MAZE_SETTINGS[row + 1][col]
                neighbouring_nodes[0] = (row + 1, col)
            elif orientation == 1:
                front_val = MAZE_SETTINGS[row][col + 1]
                neighbouring_nodes[0] = (row, col + 1)
            elif orientation == 2:
                front_val = MAZE_SETTINGS[row - 1][col]
                neighbouring_nodes[0] = (row - 1, col)
            elif orientation == 3:
                front_val = MAZE_SETTINGS[row][col - 1]
                neighbouring_nodes[0] = (row, col - 1)
            neighbouring_values[0] = front_val
        if not right_wall:
            # no wall in the right
            if orientation == 0:
                right_val = MAZE_SETTINGS[row][col + 1]
                neighbouring_nodes[1] = (row, col + 1)
            elif orientation == 1:
                right_val = MAZE_SETTINGS[row - 1][col]
                neighbouring_nodes[1] = (row - 1, col)
            elif orientation == 2:
                right_val = MAZE_SETTINGS[row][col - 1]
                neighbouring_nodes[1] = (row, col - 1)
            elif orientation == 3:
                right_val = MAZE_SETTINGS[row + 1][col]
                neighbouring_nodes[1] = (row + 1, col)
            neighbouring_values[1] = right_val
        if not left_wall:
            # no wall in the left
            if orientation == 0:
                left_val = MAZE_SETTINGS[row][col - 1]
                neighbouring_nodes[2] = (row, col - 1)
            if orientation == 1:
                left_val = MAZE_SETTINGS[row + 1][col]
                neighbouring_nodes[2] = (row + 1, col)
            if orientation == 2:
                left_val = MAZE_SETTINGS[row][col + 1]
                neighbouring_nodes[2] = (row, col + 1)
            if orientation == 3:
                left_val = MAZE_SETTINGS[row - 1][col]
                neighbouring_nodes[2] = (row - 1, col)
            neighbouring_values[2] = left_val

