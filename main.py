import matplotlib.pyplot as plt
import numpy as np
import cv2
from backend.PointRobot import PointRobot
from backend.generate_map import create_map
from backend.generate_vis import visualize
map = create_map()
kernel = np.ones((5,5), np.uint8)
map_dilate = cv2.dilate(map, kernel, iterations=1)
start = [5,195]
goal = [195,5]
robot = PointRobot(map_dilate, start, goal)
goal_node, visited, solved = robot.solve()
path = robot.backtrack(goal_node)
map = np.dstack((map*255.0, map*255.0, map*255.0)).astype(np.uint8)
if solved:
    visualize(map, visited, path, start, goal)