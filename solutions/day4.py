def main():
    with open('../data/day4/day4.txt', 'r') as file:
        lines = file.readlines()

    result1 = 0
    result2 = 0
    for line in lines:
        elf1, elf2 = line.split(',')

        elf1_start, elf1_end = get_range(elf1)
        elf2_start, elf2_end = get_range(elf2)

        # check whether each interval fully contains the other
        # first check whether interval one contains interval two
        if elf1_start <= elf2_start and elf1_end >= elf2_end:
            result1 += 1
        # second check whether interval two contains interval one
        elif elf2_start <= elf1_start and elf2_end >= elf1_end:
            result1 += 1

        # check any overlap
        if elf1_start <= elf2_start <= elf1_end:
            result2 += 1
        elif elf2_start <= elf1_start <= elf2_end:
            result2 += 1

    print(result1)
    print(result2)


def get_range(elf_range: str):
    start, end = elf_range.split('-')
    return int(start), int(end)


if __name__ == '__main__':
    main()
