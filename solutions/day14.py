import numpy as np
from numba import njit

def main():
    with open('../data/day14/day14.txt', 'r') as file:
        data = file.readlines()

    # compute the grid coordinates of the terrain
    terrain = set()
    for line in data:
        coords = line.strip().split(' -> ')

        for idx in range(len(coords) - 1):
            start_x, start_y = list(map(lambda x: int(x), coords[idx].split(',')))
            end_x, end_y = list(map(lambda x: int(x), coords[idx + 1].split(',')))

            if (diff_x := (end_x - start_x)) != 0:
                # horizontal vector
                sign_x = np.sign(diff_x)
                for x in range(start_x, end_x + sign_x, sign_x):
                    terrain.add((x, start_y))

                continue

            if (diff_y := (end_y - start_y)) != 0:
                # horizontal vector
                sign_y = np.sign(diff_y)
                for y in range(start_y, end_y + sign_y, sign_y):
                    terrain.add((start_x, y))

                continue

    # compute the initial grid with terrain
    # coordinate order is x, y
    grid = np.zeros((1000, 1000), dtype=int)

    # 0 for air, 1 for sand, 2 for terrain
    for coords in terrain:
        grid[coords[0], coords[1]] = 2

    # compute the lowest y of the terrain, after this y coordinate the sand will fall forever
    y_max = sorted(terrain, key=lambda x: x[1])[-1][1]

    sand_count = 0
    while True:
        if simulate_sand(grid, 500, 0, y_max, False):
            sand_count += 1
        else:
            break

    print(sand_count)

    # part 2
    grid2 = grid

    # add the floor to the matrix
    floor_y = y_max + 2
    grid2[:, floor_y] = 2

    sand_count2 = 0
    while True:
        if simulate_sand(grid2, 500, 0, floor_y, True):
            sand_count2 += 1
        else:
            break

    print(sand_count + sand_count2)

@njit
def simulate_sand(grid, sand_x, sand_y, y_max, part2=False):
    # returns true if sand particle stopped, false if it falls forever

    # copy the coordinates just to avoid referencing nonsense
    x = sand_x
    y = sand_y

    if grid[x, y] != 0:
        # entry point is being blocked by something
        return False

    while True:
        if part2 and (y == (y_max - 1)):
            # if a particle reached the floor it is at rest
            grid[x, y] = 1
            return True

        if y > y_max:
            # particle fell through
            return False

        if grid[x, y + 1] == 0:
            # can fall one level lower
            y += 1
            continue

        # could not fall lower, try going left
        if grid[x - 1, y + 1] == 0:
            x -= 1
            y += 1
            continue

        # could not go left, try right
        if grid[x + 1, y + 1] == 0:
            x += 1
            y += 1
            continue

        # could not move further settle here
        grid[x, y] = 1
        return True


if __name__ == '__main__':
    main()
