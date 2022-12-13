from collections import deque
import numpy as np
from typing import Dict, Tuple
import math
from itertools import product


class Node(object):

    def __init__(self, y: int, x: int, elevation: int, start: bool, end: bool):
        self.x = x
        self.y = y
        self.elevation = elevation
        self.start = start
        self.end = end
        self.edges = set()

    def add_edge(self, neighbour: 'Node'):
        self.edges.add(neighbour)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return super.__hash__(self)


def dijsktra(start: Node, all_nodes: Dict[Tuple[int, int], Node]) -> Tuple[Dict[Node, int], Dict[Node, Node]]:
    dist = {}
    prev = {}
    q = deque()

    for node in all_nodes.values():
        dist[node] = math.inf
        prev[node] = None
        q.append(node)

    dist[start] = 0

    while len(q) > 0:
        # find the smallest distance node still in q
        u = q[0]
        for node in q:
            if dist[node] < dist[u]:
                u = node

        q.remove(u)

        for neighbour in u.edges:
            if neighbour in q:
                alt = dist[u] + 1  # all connections are weight 1
                if alt < dist[neighbour]:
                    dist[neighbour] = alt
                    prev[neighbour] = u

    return dist, prev


def transpose_graph(graph_nodes: Dict[Tuple[int, int], Node]) -> Dict[Tuple[int, int], Node]:
    result = {}
    for key in graph_nodes:
        temp = graph_nodes[key]
        if key in result:
            curr_node = result[key]
        else:
            curr_node = Node(temp.y, temp.x, temp.elevation, temp.start, temp.end)
            result[key] = curr_node

        for edge in temp.edges:
            edge_coords = (edge.y, edge.x)
            if edge_coords in result:
                result[edge_coords].add_edge(curr_node)
            else:
                result[edge_coords] = Node(edge.y, edge.x, edge.elevation, edge.start, edge.end)
                result[edge_coords].add_edge(curr_node)

    return result


def main():
    with open('../data/day12/day12.txt', 'r') as file:
        data = file.readlines()


    y_size = len(data)
    x_size = len(data[0].strip())
    matrix = np.ones((y_size, x_size), dtype=int)

    # coordinate format is y, x
    start_coords = None
    end_coords = None

    start_ord = ord('a')
    end_ord = ord('z')

    for y, line in enumerate(data):
        line = line.strip()
        for x, letter in enumerate(line):
            match letter:
                case 'S':
                    start_coords = (y, x)
                    matrix[y, x] = 0
                case 'E':
                    end_coords = (y, x)
                    matrix[y, x] = end_ord % start_ord
                case _:
                    matrix[y, x] = ord(letter) % start_ord

    # create the graph from start
    start_node = None
    end_node = None
    created_nodes = {}
    for y, x in product(range(y_size), range(x_size), repeat=1):
        # check if the node already exists
        if (y, x) in created_nodes:
            curr_node = created_nodes[(y, x)]
        else:
            curr_node = Node(y, x, matrix[y, x], start_coords == (y, x), end_coords == (y, x))
            created_nodes[(y, x)] = curr_node

            # also make a reference to the end node
            if curr_node.end:
                end_node = curr_node

            if curr_node.start:
                start_node = curr_node

        curr_x = curr_node.x
        curr_y = curr_node.y
        curr_elevation = curr_node.elevation

        # only plus edged need to be checked
        edges_to_check = [(curr_y + 1, curr_x), (curr_y - 1, curr_x), (curr_y, curr_x + 1), (curr_y, curr_x - 1)]

        # matrix edge conditions
        edges_to_check = list(filter(lambda x: 0 <= x[0] < matrix.shape[0] and 0 <= x[1] < matrix.shape[1], edges_to_check))

        # check elevation conditions
        edges_to_check = list(filter(lambda x: matrix[x[0], x[1]] <= curr_elevation + 1, edges_to_check))

        for edge_coords in edges_to_check:
            if edge_coords not in created_nodes:
                # if an edge is not created yet then create it and add it to node_to_visit queue
                new_node = Node(edge_coords[0], edge_coords[1], matrix[edge_coords[0], edge_coords[1]], edge_coords == start_coords, edge_coords == end_coords)

                # mark as created
                created_nodes[edge_coords] = new_node

                # add outgoing edge from current node
                curr_node.add_edge(new_node)

                # also make a reference to the end node
                if new_node.end:
                    end_node = new_node

                if new_node.start:
                    start_node = new_node
            else:
                # edge is created then either it is in the visit queue or already visited
                edge_node = created_nodes[edge_coords]
                curr_node.add_edge(edge_node)

    # part 1
    dist, prev = dijsktra(start_node, created_nodes)
    print(dist[end_node])

    # part 2
    transposed_created_nodes = transpose_graph(created_nodes)
    transposed_end_node = [node for node in transposed_created_nodes.values() if node.end][0]
    dist2, prev2 = dijsktra(transposed_end_node, transposed_created_nodes)
    zero_nodes = [node for node in transposed_created_nodes.values() if node.elevation == 0]

    min_dist = math.inf
    for zero_node in zero_nodes:
        if dist2[zero_node] < min_dist:
            min_dist = dist2[zero_node]

    print(min_dist)


if __name__ == '__main__':
    main()
