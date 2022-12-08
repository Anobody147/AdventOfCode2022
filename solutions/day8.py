import numpy as np
import numpy.typing as npt
from itertools import product, takewhile


def main():
    with open('../data/day8/day8.txt', 'r') as file:
        data = file.readlines()

    # make the matrix
    matrix = None

    for line in data:
        numbers = np.asarray(list(map(lambda x: int(x), list(line.strip()))), dtype=int)

        if matrix is None:
            matrix = numbers
        else:
            matrix = np.vstack((matrix, numbers))

    size_y, size_x = matrix.shape
    idxs_y = list(range(size_y))
    idxs_x = list(range(size_x))

    result = []
    result2 = []
    for y, x in product(idxs_y, idxs_x, repeat=1):
        result.append(visible(x, y, matrix))
        result2.append(scenic_score(x, y, matrix))

    values, counts = np.unique(result, return_counts=True)

    print(counts[1])
    print(max(result2))


def scenic_score(x: int, y: int, matrix: npt.NDArray[int]) -> int:
    # check edge of array
    if x == 0 or x == matrix.shape[1]:
        return 0
    elif y == 0 or y == matrix.shape[0]:
        return 0

    # get the column and row of the element
    height = matrix[y, x]
    row = matrix[y]
    column = matrix[:, x]

    # check row left to right
    row_lr = np.flip(row[:x])
    row_lr_visible = list(takewhile(lambda tree_height: tree_height < height, row_lr))
    row_lr_result = len(row_lr_visible) if len(row_lr) == len(row_lr_visible) else len(row_lr_visible) + 1

    # check row right to left
    row_rl = row[x + 1:]
    row_rl_visible = list(takewhile(lambda tree_height: tree_height < height, row_rl))
    row_rl_result = len(row_rl_visible) if len(row_rl) == len(row_rl_visible) else len(row_rl_visible) + 1

    # check column top to bottom
    column_tb = np.flip(column[:y])
    column_tb_visible = list(takewhile(lambda tree_height: tree_height < height, column_tb))
    column_tb_result = len(column_tb_visible) if len(column_tb) == len(column_tb_visible) else len(column_tb_visible) + 1

    # check column bottom to top
    column_bt = column[y + 1:]
    column_bt_visible = list(takewhile(lambda tree_height: tree_height < height, column_bt))
    column_bt_result = len(column_bt_visible) if len(column_bt) == len(column_bt_visible) else len(column_bt_visible) + 1

    return row_rl_result * row_lr_result * column_bt_result * column_tb_result


def visible(x: int, y: int, matrix: npt.NDArray[int]) -> bool:
    # check edge of array
    if x == 0 or x == matrix.shape[1]:
        return True
    elif y == 0 or y == matrix.shape[0]:
        return True

    # check inside the array

    # get the column and row of the element
    height = matrix[y, x]
    row = matrix[y]
    column = matrix[:, x]

    # check row left to right
    row_lr = np.all(row[:x] < height)

    if row_lr:
        return True

    # check row right to left
    row_rl = np.all(row[x + 1:] < height)

    if row_rl:
        return True

    # check column top to bottom
    column_tb = np.all(column[:y] < height)

    if column_tb:
        return True

    # check bottom to top
    column_bt = np.all(column[y + 1:] < height)

    return column_bt


if __name__ == '__main__':
    main()