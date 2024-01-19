from abc import ABC, abstractmethod
import API
from constants import *


class Algorithm(ABC):
    def update_maze_values(self):
        for i in range(16):
            for j in range(16):
                API.setText(i, j, str(MAZE_SETTINGS[i][j]))

    @abstractmethod
    def execute(self):
        pass
