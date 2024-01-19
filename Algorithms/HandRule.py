import time

from constants import *
from Algorithms.Algorithm import Algorithm

import API


class HandRule(Algorithm):

    def execute(self):
        pass


class LeftHandRule(HandRule):

    def execute(self):
        API.ackReset()
        API.log("LEFT HAND RULE RUNNING...")


        current_position = [0, 0]
        row, col = current_position

        while True:
            if current_position[0] == CENTER and current_position[1] == CENTER:
                API.log('GG')
                break

            if not API.wallLeft():
                API.turnLeft()
                current_position[0] -= 1
            while API.wallFront():
                API.turnRight()
                current_position[0] += 1
            API.moveForward()
            current_position[1] += 1
        time.sleep(5)


class RightHandRule(HandRule):

    def execute(self):
        API.ackReset()
        API.log("RIGHT HAND RULE RUNNING...")

        current_position = [0, 0]
        row, col = current_position

        while True:
            if current_position[0] == CENTER and current_position[1] == CENTER:
                API.log('GG')
                break

            if not API.wallRight():
                API.turnRight()
                current_position[0] += 1
            while API.wallFront():
                API.turnLeft()
                current_position[0] -= 1
            API.moveForward()
            current_position[1] += 1

