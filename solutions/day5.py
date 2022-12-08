from collections import deque
from copy import deepcopy


def main():
    with open('../data/day5/day5.txt', 'r') as file:
        data = file.read()

    stack_data, movement_data = data.split('\n\n')
    stack_lines = stack_data.split('\n')[:-1] # remove stack line number
    movement_lines = movement_data.split('\n')

    # we have nine stacks
    stacks = [deque() for _ in range(9)]

    # parse the stacks
    for line in stack_lines:
        for idx in range(9):
            crate = line[idx * 4 + 1]
            if crate != ' ':
                stacks[idx].append(crate)

    # copy for second part
    stacks2 = deepcopy(stacks)

    # manipulate the stack according to the instructions
    for line in movement_lines:
        line = line.strip()
        splits = line.split(' ')
        number_crates = int(splits[1])
        from_stack = int(splits[3]) - 1
        to_stack = int(splits[5]) - 1

        # part 1
        for idx in range(number_crates):
            stacks[to_stack].appendleft(stacks[from_stack].popleft())

        # part 2
        crates = list(stacks2[from_stack])[:number_crates]
        stacks2[from_stack] = deque(list(stacks2[from_stack])[number_crates:])
        stacks2[to_stack] = deque(crates + list(stacks2[to_stack]))

    result_str = ''
    result_str2 = ''
    for idx in range(len(stacks)):
        result_str += stacks[idx][0]
        result_str2 += stacks2[idx][0]

    print(result_str)
    print(result_str2)


if __name__ == '__main__':
    main()