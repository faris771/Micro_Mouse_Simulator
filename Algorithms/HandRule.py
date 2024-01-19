import time

from constants import *
from Algorithms.Algorithm import Algorithm

import API


class HandRule(Algorithm):

    def execute(self):
        pass


class LeftHandRule(HandRule):
    def check_end_point(self, current_position):
        if (current_position[0] == CENTER and current_position[0] == CENTER) or (
                current_position[0] == CENTER - 1 and current_position[0] == CENTER - 1) or (
                current_position[0] == CENTER - 1 and current_position[0] == CENTER) or (
                current_position[0] == CENTER and current_position[0] == CENTER - 1):
            return True

    def execute(self):
        # API.ackReset()
        API.log("LEFT HAND RULE RUNNING...")

        current_position = [0, 0]
        row, col = current_position

        while True:

            # if self.check_end_point(current_position):
            #     break

            # API.setColor(current_position[1], current_position[0], 'B')

            if not API.wallLeft():
                API.turnLeft()
                current_position[0] -= 1
            while API.wallFront():
                API.turnRight()
                current_position[0] += 1
                # API.setColor(current_position[1], current_position[0], 'G')

            API.moveForward()
            current_position[0] += 1

            # API.setColor(current_position[1], current_position[0], 'G')


class RightHandRule(HandRule):
    def check_end_point(self, current_position):
        if (current_position[0] == CENTER and current_position[0] == CENTER) or (
                current_position[0] == CENTER - 1 and current_position[0] == CENTER - 1) or (
                current_position[0] == CENTER - 1 and current_position[0] == CENTER) or (
                current_position[0] == CENTER and current_position[0] == CENTER - 1):
            return True

    def execute(self):

        # API.ackReset()
        API.log("RIGHT HAND RULE RUNNING...")

        current_position = [0, 0]
        row, col = current_position

        while True:

            if self.check_end_point(current_position):
                break

            if not API.wallRight():
                API.turnRight()
                current_position[0] += 1
                API.setColor(current_position[1], current_position[0], 'G')

            while API.wallFront():
                API.turnLeft()
                current_position[0] -= 1
                API.setColor(current_position[1], current_position[0], 'G')

            API.moveForward()
            current_position[1] += 1
            API.setColor(current_position[1], current_position[0], 'G')
