import re
from typing import List, Tuple, Dict
import math
from collections import deque


class Node(object):

    def __init__(self, name, flow):
        self.name = name
        self.flow = flow
        self.edges = []
        self.opened = False

    def add_edge(self, edge: 'Node'):
        if edge is not None:
            self.edges.append(edge)

    def __str__(self):
        return f'{self.name}-{self.flow}'

    def __hash__(self):
        return super.__hash__(self)


def main():
    with open('../data/day16/test16.txt', 'r') as file:
        data = file.readlines()

    # parse the input data
    nodes = []
    flows = []
    edges = []
    for line in data:
        found_nodes = re.findall(r'[A-Z]{2}', line.strip())
        flow = re.findall(r'[0-9]+', line.strip())

        # first found node name is the current node
        nodes.append(found_nodes[0])

        flows.append(int(flow[0]))

        node_edges = []
        for idx in range(1, len(found_nodes)):
            node_edges.append(found_nodes[idx])

        edges.append(tuple(node_edges))

    node_edges = {}
    node_flows = {}
    for node, edge_list, flow in zip(nodes, edges, flows):
        node_edges[node] = edge_list
        node_flows[node] = flow

    # construct the nodes
    node_objects = {}
    for node, flow in zip(nodes, flows):
        node_objects[node] = Node(node, flow)

    # add the edges to the nodes
    for node, edge_list in zip(nodes, edges):
        for edge in edge_list:
            node_objects[node].add_edge(node_objects[edge])

    # solve loop
    time_left = 30
    curr_node = node_objects['AA']
    curr_release = 0

    while time_left > 0:

        # compute the distances and paths
        distances, previous = dijsktra(node_objects, curr_node)

        # compute the values of each node
        node_values = []
        for node in node_objects.values():

            # check that flow is not 0 and is not opened already
            if node.flow == 0 or node.opened:
                continue

            # compute the value of a node
            node_values.append((node, node.flow * (time_left - 1 - distances[node])))

        # sort the list according to the node values
        node_values.sort(key=lambda x: x[1], reverse=True)

        if len(node_values) < 1:
            # no new nodes left to explore
            break

        target_node = node_values[0][0]

        # check if opening the current node valve would be worth delaying
        if not curr_node.opened and (curr_node.flow * (time_left - 1)) >= target_node.flow:
            print(f'Valve {curr_node.name} is open, releasing {curr_node.flow * (time_left - 1)} pressure')
            curr_node.opened = True
            curr_release += curr_node.flow * (time_left - 1)
            time_left = time_left - 1
            continue

        # check if any of the neighbours would be worth delaying for
        delay_nodes = []
        for node in curr_node.edges:
            if (node.flow * (time_left - 2)) >= (target_node.flow * 2) and not node.opened:
                delay_nodes.append((node, node.flow * (time_left - 2)))

        delay_nodes.sort(key=lambda x: x[1], reverse=True)

        if len(delay_nodes) > 0:

            # check to make sure that the detour does not increase the distance to the target in excess of it's value
            delay_node = None
            for delay_node in delay_nodes:
                node = delay_node[0]
                node_value = delay_node[1]
                delay_distances, delay_previous = dijsktra(node_objects, node)
                if (delay_distances[target_node] - distances[target_node]) * target_node.flow > node_value:
                    continue
                else:
                    delay_node = node
                    break

            if delay_node is not None:
                print(f'Bypas Valve {delay_node.name} is open, releasing {delay_node.flow * (time_left - 2)} pressure')
                curr_release += delay_node.flow * (time_left - 2)
                delay_node.opened = True
                time_left -= 2
                curr_node = delay_node
                continue

        # if not go the node next on the path
        prev_node = previous[target_node]
        while prev_node is not curr_node:
            target_node = prev_node
            prev_node = previous[prev_node]

        # found the next step so take it
        curr_node = target_node
        time_left -= 1

    print(curr_release)


def dijsktra(graph: Dict[str, Node], source: Node) -> Tuple[Dict[Node, int], Dict[Node, Node]]:

    dist = {}
    prev = {}
    Q = []
    for v in graph.values():
        dist[v] = math.inf
        prev[v] = None
        Q.append(v)
    dist[source] = 0

    while len(Q) > 0:
        u = None
        u_dist = math.inf
        for v in Q:
            if dist[v] < u_dist:
                u = v
                u_dist = dist[v]
        Q.remove(u)

        for v in u.edges:
            if v not in Q:
                continue

            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist, prev

if __name__ == '__main__':
    main()
