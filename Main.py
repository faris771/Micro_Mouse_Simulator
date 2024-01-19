import API
import heapq
import sys
import time
from constants import *
from Algorithms.Floodfill import FloodFill
from Algorithms.HandRule import LeftHandRule, RightHandRule


def color_center():
    API.setColor(CENTER, CENTER, "G")
    API.setColor(CENTER - 1, CENTER, "G")
    API.setColor(CENTER - 1, CENTER - 1, "G")
    API.setColor(CENTER, CENTER - 1, "G")


def main():

    API.log("Running...")
    API.setColor(0, 0, "G")
    API.setText(0, 0, "start")

    color_center()


    API.setText(CENTER, CENTER, "Goal")

    floodfill = FloodFill()
    leftHandRule = LeftHandRule()
    rightHandRule = RightHandRule()


    floodfill.execute()
    # time.sleep(3)
    # leftHandRule.execute()
    # time.sleep(3)
    # rightHandRule = RightHandRule()
    # rightHandRule.execute()
    # time.sleep(3)







if __name__ == "__main__":
    main()