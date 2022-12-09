from typing import Tuple, List


def main():
    with open('../data/day9/day9.txt', 'r') as file:
        data = file.readlines()

    # order is x,y
    head_coords = (0, 0)
    tail_coords = (0, 0)
    snake_coords = [(0, 0) for _ in range(10)]

    head_history = [head_coords]
    tail_history = [tail_coords]
    snake_tail_history = [snake_coords[-1]]

    for line in data:
        command, distance = line.strip().split()
        distance = int(distance)

        match command:
            case 'U':
                for _ in range(distance):
                    head_coords = (head_coords[0], head_coords[1] + 1)
                    head_history.append(head_coords)

                    if not touching(head_coords, tail_coords):
                        tail_coords = update_tail(head_coords, tail_coords)
                        tail_history.append(tail_coords)

                    # part 2
                    update_snake(0, 1, snake_coords, snake_tail_history)

            case 'D':
                for _ in range(distance):
                    head_coords = (head_coords[0], head_coords[1] - 1)
                    head_history.append(head_coords)

                    if not touching(head_coords, tail_coords):
                        tail_coords = update_tail(head_coords, tail_coords)
                        tail_history.append(tail_coords)

                    # part 2
                    update_snake(0, -1, snake_coords, snake_tail_history)
            case 'L':
                for _ in range(distance):
                    head_coords = (head_coords[0] - 1, head_coords[1])
                    head_history.append(head_coords)

                    if not touching(head_coords, tail_coords):
                        tail_coords = update_tail(head_coords, tail_coords)
                        tail_history.append(tail_coords)

                    # part 2
                    update_snake(-1, 0, snake_coords, snake_tail_history)
            case 'R':
                for _ in range(distance):
                    head_coords = (head_coords[0] + 1, head_coords[1])
                    head_history.append(head_coords)

                    if not touching(head_coords, tail_coords):
                        tail_coords = update_tail(head_coords, tail_coords)
                        tail_history.append(tail_coords)

                    # part 2
                    update_snake(1, 0, snake_coords, snake_tail_history)
            case _:
                raise Exception(f"Unknown command: {command}")

    print(len(list(set(tail_history))))
    print(len(list(set(snake_tail_history))))


def touching(head: Tuple[int, int], tail: Tuple[int, int]) -> bool:
    # check overlapping
    if head == tail:
        return True

    # check if touching, at most a diff of one in one both dimensions
    if abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1:
        return True

    return False


def update_snake(move_x: int, move_y: int,
                 snake: List[Tuple[int, int]],
                 tail_history: List[Tuple[int, int]]):

    snake[0] = (snake[0][0] + move_x, snake[0][1] + move_y)
    for idx in range(1, len(snake)):
        if not touching(snake[idx - 1], snake[idx]):
            snake[idx] = update_tail(snake[idx - 1], snake[idx])

            if idx == len(snake) - 1:
                tail_history.append(snake[-1])
        else:
            # once a point in the chain does not change the rest will not change as well
            break

    pass


def update_tail(head: Tuple[int, int], tail: Tuple[int, int]) -> Tuple[int, int]:
    new_tail = (tail[0], tail[1])

    diff_x = head[0] - tail[0]
    diff_y = head[1] - tail[1]

    if diff_x != 0:
        new_tail = (new_tail[0] + sign(diff_x), new_tail[1])

    if diff_y != 0:
        new_tail = (new_tail[0], new_tail[1] + sign(diff_y))

    return new_tail


def sign(number: int):
    return 1 if number >= 0 else -1


if __name__ == '__main__':
    main()