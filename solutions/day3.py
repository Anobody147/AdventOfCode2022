from functools import reduce


def main():
    with open('../data/day3/day3.txt', 'r') as file:
        lines = file.readlines()

    result = 0
    for line in lines:
        line = line.strip()
        first, second = line[:len(line) // 2], line[len(line) // 2:]
        assert len(first) == len(second)

        # convert to sets and priority
        first = set(list(map(convert_ordinal, first)))
        second = set(list(map(convert_ordinal, second)))

        # get intersection
        intersection = first.intersection(second)

        result += sum(intersection)

    print(result)

    second_result = 0
    for idx in range(0, len(lines), 3):
        slice = lines[idx: idx + 3]

        slice = [set(list(map(convert_ordinal, line.strip()))) for line in slice]

        intersection = reduce(lambda x, y: x.intersection(y), slice)

        second_result += sum(intersection)

    print(second_result)


def convert_ordinal(letter: str):
    if letter.isupper():
        return ord(letter) % 64 + 26
    else:
        return ord(letter) % 96


if __name__ == '__main__':
    main()
