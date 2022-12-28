import re
from typing import List, Tuple, Dict
from itertools import product
import math
from functools import cache


def main():
    with open('../data/day16/day16.txt', 'r') as file:
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

    # compute the distances between all the nodes
    node_distances = floyd_warshall(nodes, node_edges)

    @cache
    def DFS(nodes, curr_node, time_left) -> int:

        values = [0]
        for idx, node in enumerate(nodes):
            if (time_left - node_distances[curr_node, node]) > 0:
                node_copy = nodes[:idx] + nodes[idx + 1:]

                new_time_left = time_left - node_distances[curr_node, node] - 1
                new_release = (new_time_left * node_flows[node])

                value = new_release + DFS(node_copy, node, new_time_left)
                values.append(value)

        return max(values)

    @cache
    def DFS_2(nodes, curr_node, time_left) -> int:

        # compete against the regular version to find the best version
        values = [DFS(nodes, 'AA', 26)]
        for idx, node in enumerate(nodes):
            if (time_left - node_distances[curr_node, node]) > 0:
                node_copy = nodes[:idx] + nodes[idx + 1:]

                new_time_left = time_left - node_distances[curr_node, node] - 1
                new_release = (new_time_left * node_flows[node])

                value = new_release + DFS_2(node_copy, node, new_time_left)
                values.append(value)

        return max(values)

    # DFS
    filtered_nodes = tuple(filter(lambda x: node_flows[x] > 0, nodes))
    result = DFS(filtered_nodes, 'AA', 30)

    print(result)

    # part 2
    filtered_nodes = tuple(filter(lambda x: node_flows[x] > 0, nodes))
    result_2 = DFS_2(filtered_nodes, 'AA', 26)

    print(result_2)


def floyd_warshall(nodes: List[str], edges: Dict[str, Tuple[str, ...]]) -> Dict[Tuple[str, str], int]:
    dist = {}
    for x, y in product(nodes, nodes, repeat=1):
        dist[x, y] = math.inf

    for node in nodes:
        for edge in edges[node]:
            dist[node, edge] = 1

    for node in nodes:
        dist[node, node] = 0

    for k, i, j in product(nodes, nodes, nodes, repeat=1):
        if dist[i, j] > dist[i, k] + dist[k, j]:
            dist[i, j] = dist[i, k] + dist[k, j]

    return dist


if __name__ == '__main__':
    main()
