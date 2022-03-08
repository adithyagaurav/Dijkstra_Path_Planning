import numpy as np
from queue import PriorityQueue
from backend.Node import Node


class PointRobot:
    def __init__(self, map, start_pos, goal_pos):
        self.map = map
        self.size_y, self.size_x = self.map.shape[:2]
        self.start_x, self.start_y = start_pos[0], start_pos[1]
        self.goal_x, self.goal_y = goal_pos[0], goal_pos[1]

    def get_neighbors(self, curr_node):
        i, j = curr_node.x, curr_node.y
        actions = [(i, j + 1), (i + 1, j), (i - 1, j), (i, j - 1), (i + 1, j + 1), (i - 1, j - 1), (i - 1, j + 1),
                   (i + 1, j - 1)]
        valid_neighbor_nodes = []
        count = 0
        for action in actions:
            if action[0] >= self.size_x or action[0] < 0 or action[1] >= self.size_y or action[1] < 0:
                continue

            if self.map[action[1]][action[0]] == 0:
                cost = 1
                if count > 3:
                    cost = 1.4
                new_node = Node((action[0], action[1]), cost=cost, parent=curr_node)
                valid_neighbor_nodes.append(new_node)
            count += 1
        return valid_neighbor_nodes

    def is_visited(self, curr_node, visited):
        for node in visited:
            if curr_node.x == node.x and curr_node.y == node.y:
                return True
        return False

    def is_solvable(self):
        if self.goal_x < 0 or self.goal_x >= self.size_x or \
                self.goal_y < 0 or self.goal_y >= self.size_y or \
                self.map[self.goal_y][self.goal_x] == 1 or self.map[self.start_y][self.start_x] == 1:
            return False
        return True

    def solve(self):
        if not self.is_solvable():
            print("Path Not Found!")
            return None, None, False
        node_queue = PriorityQueue()
        visited = set([])
        cost_pixels = {}
        for i in range(self.size_y):
            for j in range(self.size_x):
                cost_pixels[(i, j)] = float('inf')

        cost_pixels[(self.start_x, self.start_y)] = 0
        start_node = Node((self.start_x, self.start_y), 0, None)
        visited.add((self.start_x, self.start_y))
        visited_array = []
        node_queue.put([start_node.cost, start_node.pos, start_node])

        while not node_queue.empty():
            _, _, curr_node = node_queue.get()
            if curr_node.x == self.goal_x and curr_node.y == self.goal_y:
                print("Goal reached!")
                return curr_node, visited_array, True

            valid_neighbor_nodes = self.get_neighbors(curr_node)
            for neighbor_node in valid_neighbor_nodes:
                if neighbor_node.pos in visited:
                    cost_new = neighbor_node.cost + cost_pixels[(curr_node.x, curr_node.y)]
                    if cost_new < cost_pixels[(neighbor_node.x, neighbor_node.y)]:
                        cost_pixels[(neighbor_node.x, neighbor_node.y)] = cost_new
                        neighbor_node.parent = curr_node
                else:
                    visited.add((neighbor_node.x, neighbor_node.y))
                    visited_array.append(((neighbor_node.x, neighbor_node.y)))
                    cost = cost_pixels[(curr_node.x, curr_node.y)] + neighbor_node.cost
                    new_node = Node((neighbor_node.x, neighbor_node.y), cost, curr_node)
                    cost_pixels[(neighbor_node.x, neighbor_node.y)] = cost
                    node_queue.put([new_node.cost, new_node.pos, new_node])

        return None, None, False
    def backtrack(self, goal_node):
        parent_node = goal_node.parent
        path = []
        while parent_node:
            path.append(parent_node.pos)
            parent_node = parent_node.parent
        return reversed(path)