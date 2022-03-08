import numpy as np

class Node:
    def __init__(self, pos, cost, parent):  # creating objects for position, cost and parent information
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.cost = cost
        self.parent = parent