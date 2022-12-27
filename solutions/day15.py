import re
from typing import Tuple, Union
from collections import deque


def main():
    with open('../data/day15/day15.txt', 'r') as file:
        data = file.readlines()

    # parse the coordinates, coordinates in x, y format
    sensors = []
    beacons = []
    for line in data:
        sensor, beacon = line.strip().split(':')

        sensor_x, sensor_y = re.findall(r'-?[0-9]+', sensor)
        beacon_x, beacon_y = re.findall(r'-?[0-9]+', beacon)

        sensors.append((int(sensor_x), int(sensor_y)))
        beacons.append((int(beacon_x), int(beacon_y)))

    # get the distances for the sensor beacon pairs
    distances = []
    for sensor, beacon in zip(sensors, beacons):
        distances.append(manhattan(sensor, beacon))

    # get the intervals of the different beacons
    y_pos = 2000000
    intervals = []
    for sensor, distance in zip(sensors, distances):
        interval = interval_at_position(sensor, distance, y_pos, 1)
        if interval is not None:
            intervals.append(interval)

    # add in the beacon positions on that axis to be folded in
    intervals = add_beacons(intervals, beacons, y_pos, 1)

    folded_intervals = fold_intervals(intervals)

    res = 0
    for interval in folded_intervals:
        res += (interval[1] - interval[0])

    print('part 1 ', res)

    # part 2
    search_interval = (0, 4000000)
    coord_y = None
    coord_x = None
    for idy in range(4000000 + 1):

        exclude = False
        pos_intervals = []
        for sensor, distance in zip(sensors, distances):
            intervals_position = interval_at_position(sensor, distance, idy, 1)

            if intervals_position is None:
                continue

            if subinterval(search_interval, intervals_position):
                exclude = True
                break

            pos_intervals.append(intervals_position)

        if exclude:
            continue
        else:
            pos_intervals = add_beacons(pos_intervals, beacons, idy, 1)
            pos_intervals = fold_intervals(pos_intervals)

            if len(pos_intervals) != 1:
                coord_y = idy
                coord_x = pos_intervals[0][1] + 1
                break

            if not subinterval(search_interval, pos_intervals[0]):
                coord_y = idy
                coord_x = pos_intervals[0][1] + 1
                break

    print('part 2', coord_x * 4000000 + coord_y)


def add_beacons(intervals, beacons, pos, axis):
    for beacon in beacons:
        if beacon[axis] == pos:
            intervals.append((beacon[other_axis(axis)], beacon[other_axis(axis)]))

    return intervals


def interval_at_position(sensor: Tuple[int, int], distance: int, axis_position: int, axis: int = 1) -> Union[Tuple[int, int], None]:
    beacon_pos = sensor[axis]
    beacon_pos_other = sensor[other_axis(axis)]
    diff = abs(beacon_pos - axis_position)

    # check if the position is out of range
    if diff > distance:
        return None

    # if the distance just barely reaches then just the position itself is included
    if diff == distance:
        return beacon_pos_other, beacon_pos_other

    return beacon_pos_other - (distance - diff), beacon_pos_other + (distance - diff)


def manhattan(coord1: Tuple[int, int], coord2: Tuple[int, int]):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


def overlapping(interval1: Tuple[int, int], interval2: Tuple[int, int]) -> bool:
    return interval1[0] <= interval2[0] <= interval1[1] or interval2[0] <= interval1[0] <= interval2[1]


def merge_intervals(interval1: Tuple[int, int], interval2: Tuple[int, int]) -> Tuple[int, int]:
    return min(interval1[0], interval2[0]), max(interval1[1], interval2[1])


def other_axis(axis: int):
    return 1 if axis == 0 else 0


def subinterval(interval1, interval2) -> bool:
    # is interval1 a sub-interval of interval2
    return interval2[0] <= interval1[0] and interval2[1] >= interval1[1]


def fold_intervals(intervals):
    # fold the intervals onto themselves
    while True:
        intervals_len = len(intervals)
        queue = deque(intervals)
        result = []
        while True:

            if len(queue) == 0:
                break

            target_interval = queue.popleft()
            merged_intervals = []
            for interval in queue:
                if overlapping(target_interval, interval):
                    target_interval = merge_intervals(target_interval, interval)
                    merged_intervals.append(interval)

            # remove the merged in intervals from the queue
            for interval in merged_intervals:
                queue.remove(interval)

            result.append(target_interval)

        if intervals_len == len(result):
            break
        else:
            intervals = result

    return result


if __name__ == '__main__':
    main()