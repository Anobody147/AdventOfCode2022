import numpy as np


def main():
    with open('../data/day1/calories.txt', 'r') as file:
        lines = file.readlines()

    elfs = []
    cals = []
    for line in lines:
        if line != '\n':
            cals.append(int(line))
        else:
            elfs.append(cals)
            cals = []
    elfs_cals = [sum(calories) for calories in elfs]
    idx_max = np.argmax(elfs_cals)
    print(elfs_cals[idx_max])

    idx_sort = np.argsort(elfs_cals)
    print(sum(np.asarray(elfs_cals)[idx_sort[-3:]]))


if __name__ == '__main__':
    main()
