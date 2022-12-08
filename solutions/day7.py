from collections import deque
from functools import reduce
from typing import List, Tuple, Union, Dict
from enum import Enum
from os import path
import numpy as np


class NodeType(Enum):
    DIR = 1
    FILE = 2


class Node(object):

    def __init__(self, node_type: NodeType = NodeType.DIR,
                 node_size: int = 0, name: str = '/',
                 parent: 'Node' = None):
        self.node_type: NodeType = node_type
        self.parent: Node = parent
        self.size: int = node_size
        self.name: str = name
        self.children: List[Node] = []

    def add_child(self, child: 'Node' = None) -> None:
        if child is None:
            raise Exception('Child is None')

        # check for duplicate children
        if reduce(lambda x, y: x or y, map(lambda x: x.equal(child), self.children), False):
            return

        self.children.append(child)

    def get_size(self) -> int:
        if self.node_type is NodeType.DIR:
            return sum(list(map(lambda x: x.get_size(), self.children)))
        else:
            return self.size

    def find_child(self, child_name: str) -> Union['Node', None]:
        for child in self.children:
            if child.name == child_name:
                return child

        return None

    def get_full_path(self) -> str:
        result: List['Node'] = []
        curr_node = self
        while True:
            if curr_node is not None:
                result.append(curr_node)
                curr_node = curr_node.parent
            else:
                break

        return path.join(*list(reversed(list(map(lambda x: x.name, result)))))

    def is_root(self) -> bool:
        return self.parent is None

    def equal(self, node: 'Node' = None) -> bool:
        if node is None:
            return False

        return node.node_type == self.node_type and \
            node.size == self.size and \
            node.name == self.name and \
            node.parent == self.parent


def tree_walk(node: Node, result: List[int]) -> List[int]:
    node_size = node.get_size()
    if node_size <= 100000 and node.node_type == NodeType.DIR:
        result.append(node_size)

    for child in node.children:
        tree_walk(child, result)

    return result


def get_directory_sizes(node: Node, result: Dict[str, int]) -> Dict[str, int]:
    if node.node_type == NodeType.DIR:
        result[node.get_full_path()] = node.get_size()

    for child in node.children:
        get_directory_sizes(child, result)

    return result


def main():
    with open('../data/day7/day7.txt', 'r') as file:
        data = file.readlines()

    # parse the directory structure
    idx = 0
    root = Node()
    curr_node = root
    while idx < len(data):
        command_splits = data[idx].strip().split()
        command = command_splits[1]
        match command:
            case 'ls':
                idx += 1
                while not data[idx].startswith('$'):
                    line = data[idx].strip()
                    if line.startswith('dir'):
                        # directory
                        dir_name = line.strip().split()[1]
                        new_node = Node(NodeType.DIR, 0, dir_name, curr_node)
                        curr_node.add_child(new_node)
                    else:
                        # file
                        splits = line.strip().split()
                        file_size = int(splits[0])
                        file_name = splits[1]
                        new_node = Node(NodeType.FILE, file_size, file_name, curr_node)
                        curr_node.add_child(new_node)

                    idx += 1
                    if idx >= len(data):
                        break

            case 'cd':
                cd_target = command_splits[2]
                match cd_target:
                    case '..':
                        if curr_node == root:
                            pass
                        else:
                            curr_node = curr_node.parent
                    case '/':
                        curr_node = root
                    case _:
                        target_node = curr_node.find_child(cd_target)
                        if target_node is None:
                            raise Exception(f'No such directory exists, curr_node: {curr_node.get_full_path()}; '
                                            f'target_node: {cd_target}')

                        curr_node = target_node

                idx += 1

    # part 1
    tree_walk_result = tree_walk(root, [])
    print(sum(tree_walk_result))

    # part 2

    directory_size = get_directory_sizes(root, {})

    # get the current used data amount
    occupied = directory_size['/']
    needed_free = 30000000 - (70000000 - occupied)

    # find the smallest directory meeting the criteria
    directory_size = np.asarray(sorted(list(directory_size.values())))
    directory_size = directory_size[directory_size >= needed_free]

    deleted_directory_size = directory_size[0]
    print(deleted_directory_size)


if __name__ == '__main__':
    main()
