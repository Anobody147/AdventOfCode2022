from enum import Enum
from functools import cmp_to_key


class Order(Enum):
    ORDERED = 1
    NOT_ORDERED = 2
    UNKNOWN = 3


def main():
    with open('../data/day13/day13.txt', 'r') as file:
        data = file.read()

    string_pairs = data.split('\n\n')
    pairs = {}

    for idx, pair in enumerate(string_pairs):
        packet1, packet2 = pair.split()
        packet1, packet2 = packet1.strip(), packet2.strip()

        pack1 = eval(packet1)
        pack2 = eval(packet2)

        pairs[idx + 1] = (pack1, pack2)

    in_order = []

    for key in pairs:
        packet1, packet2 = pairs[key]

        packets_ordered = ordered(packet1, packet2)

        match packets_ordered:
            case Order.ORDERED:
                in_order.append(key)
            case Order.NOT_ORDERED:
                pass
            case Order.UNKNOWN:
                in_order.append(key)

    print('part 1', sum(in_order))

    # part 2
    divider1 = [[2]]
    divider2 = [[6]]

    packets = []
    for value in pairs.values():
        packets.append(value[0])
        packets.append(value[1])

    packets.append(divider1)
    packets.append(divider2)

    sorted_packets = sorted(packets, key=cmp_to_key(comparison), reverse=True)

    divider1_idx = sorted_packets.index(divider1) + 1
    divider2_idx = sorted_packets.index(divider2) + 1

    print('part 2', divider1_idx * divider2_idx)


def comparison(left, right) -> int:
    packets_ordered = ordered(left, right)

    match packets_ordered:
        case Order.ORDERED:
            return 1
        case Order.NOT_ORDERED:
            return -1
        case Order.UNKNOWN:
            return 1


def ordered(left, right) -> Order:
    idx = 0
    while True:
        if len(left) == idx == len(right):
            return Order.UNKNOWN

        # if left list ran out first or both list ran out = ordered
        if idx == len(left):
            return Order.ORDERED if idx <= len(right) else Order.NOT_ORDERED

        # if the right list ran out first = not ordered, if the same length = ordered
        if idx == len(right):
            return Order.ORDERED if idx == len(left) else Order.NOT_ORDERED

        # now check values
        left_type = type(left[idx])
        right_type = type(right[idx])

        if left_type == list and right_type == list:
            lists_ordered = ordered(left[idx], right[idx])
            # only if lists do not compare the same do we have an unordered list
            match lists_ordered:
                case Order.ORDERED:
                    return Order.ORDERED
                case Order.NOT_ORDERED:
                    return Order.NOT_ORDERED
                case Order.UNKNOWN:
                    pass

        elif left_type == int and right_type == int:
            if left[idx] < right[idx]:
                return Order.ORDERED
            elif left[idx] > right[idx]:
                return Order.NOT_ORDERED
            # if equal it tells us nothing
        else:
            # mixed types, so convert the int to a list
            left_element = left[idx]
            right_element = right[idx]

            if left_type == int:
                left_element = [left_element]

            if right_type == int:
                right_element = [right_element]

            lists_ordered = ordered(left_element, right_element)
            match lists_ordered:
                case Order.ORDERED:
                    return Order.ORDERED
                case Order.NOT_ORDERED:
                    return Order.NOT_ORDERED
                case Order.UNKNOWN:
                    pass

        idx += 1


if __name__ == '__main__':
    main()