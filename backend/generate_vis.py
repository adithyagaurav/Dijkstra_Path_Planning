import numpy as np
import cv2

def visualize(map, visited, path, start, goal):
    vid = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 60, (400,250))
    count=0
    for node_pos in visited:
        x, y = node_pos[0], node_pos[1]
        map[y][x] = (0, 215, 255)
        count+=1
        if count%100==0:
            map = cv2.circle(map, (start[0], start[1]), radius=2, color=(255, 0, 0), thickness=-1)
            map = cv2.circle(map, (goal[0], goal[1]), radius=2, color=(0, 255, 0), thickness=-1)
            vid.write(map)
    for node_pos in path:
        x, y = node_pos[0], node_pos[1]
        map[y][x] = (0, 0, 255)
        map = cv2.circle(map, (start[0], start[1]), radius=2, color=(255, 0, 0), thickness=-1)
        map = cv2.circle(map, (goal[0], goal[1]), radius=2, color=(0, 255, 0), thickness=-1)

        vid.write(map)
    vid.release()