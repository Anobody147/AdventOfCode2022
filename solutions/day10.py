import numpy as np

def main():
    with open('../data/day10/day10.txt', 'r') as file:
        data = file.readlines()

    cycle = 1
    register_value = 1
    check_cycles = [20, 60, 100, 140, 180, 220]
    signal_strength = []

    # dimensions are y,x
    display_grid = np.zeros((6, 40), dtype=bool)

    def update_cycle():
        if cycle in check_cycles:
            signal_strength.append(cycle * register_value)

        # get current beam coordinates
        beam_y = (cycle - 1) // display_grid.shape[1]
        beam_x = (cycle - 1) % display_grid.shape[1]

        # check if sprite in range of beam
        sprite_xs = list(filter(lambda x: 0 <= x < display_grid.shape[1], [register_value - 1, register_value, register_value + 1]))
        if beam_x in sprite_xs:
            display_grid[beam_y, beam_x] = True

        return cycle + 1

    for line in data:
        if line.startswith('addx'):
            command, param = line.strip().split()

            for _ in range(2):
                cycle = update_cycle()

            register_value += int(param)
        else:
            cycle = update_cycle()

    # part 1
    print(sum(signal_strength))

    # part 2
    for y_axis in display_grid:
        for x_axis in y_axis:
            if x_axis:
                print('#', end='')
            else:
                print(' ', end='')
        print()


if __name__ == '__main__':
    main()