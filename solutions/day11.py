from typing import List, Callable
from math import lcm


class Monkey(object):

    def __init__(self, id: int, items: List[int], op: Callable[[int], int],
                 divisor: int, true_id: int, false_id: int, part: int):
        self.id = id
        self.items = items
        self.op = op
        self.divisor = divisor
        self.true_id = true_id
        self.false_id = false_id
        self.inspections = 0
        self.part = part

    def process_turn(self, monkey_list: List['Monkey'], monkey_lcm: int) -> None:
        for item in self.items:
            if self.part == 1:
                new_item = self.op(item) // 3
            elif self.part == 2:
                new_item = self.op(item)
                # this took far too long to figure out...
                new_item %= monkey_lcm
            else:
                raise Exception(f'Unknown part {self.part}')

            if (new_item % self.divisor) == 0:
                monkey_list[self.true_id].receive_item(new_item)
            else:
                monkey_list[self.false_id].receive_item(new_item)

            self.inspections += 1

        self.items = []

    def receive_item(self, item: int):
        self.items.append(item)

    def __str__(self):
        return str({'id': self.id, 'items': self.items, 'op': self.op,
                    'divisor': self.divisor, 'true_id': self.true_id, 'false_id': self.false_id,
                    'inspections': self.inspections})


def main(part):
    with open('../data/day11/day11.txt', 'r') as file:
        data = file.read()

    # parse the data
    monkey_descriptions = data.split('\n\n')

    monkeys = []
    divisors = []
    for desc in monkey_descriptions:
        lines = [line.strip() for line in desc.splitlines()]

        # line 0 is monkey id
        monkey_id = int(lines[0].split()[1][:-1])

        # line 1 is starting items
        monkey_items = [int(item.strip()) for item in lines[1][16:].split(',')]

        # line 2 is op... yes this is evil, but this is not going to production...
        monkey_op = eval(f'lambda old: {lines[2][17:]}')

        # line 3 is divisability test
        divisor = int(lines[3][19:])
        divisors.append(divisor)

        # line 4 is true target
        true_target = int(lines[4][25:])

        # line 5 is false target
        false_target = int(lines[5][25:])

        new_monkey = Monkey(monkey_id, monkey_items, monkey_op, divisor, true_target, false_target, part)
        monkeys.append(new_monkey)

    monkey_lcm = lcm(*divisors)

    # process the monkey rounds
    rounds = 20 if part == 1 else 10000
    for round in range(rounds):
        for monkey in monkeys:
            monkey.process_turn(monkeys, monkey_lcm)

    # find the monkey business level
    inspections = sorted(list(map(lambda x: x.inspections, monkeys)))
    print(f'part {part}:', inspections[-1] * inspections[-2])


if __name__ == '__main__':
    main(part=1)
    main(part=2)
