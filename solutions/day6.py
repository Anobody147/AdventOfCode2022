from collections import deque


def main():
    with open('../data/day6/day6.txt', 'r') as file:
        data = file.read()

    data = data.strip()
    queue_packet = deque([], maxlen=4)
    packet_found = False
    queue_message = deque([], maxlen=14)
    for idx in range(len(data)):
        queue_packet.append(data[idx])
        queue_message.append(data[idx])

        if len(set(queue_packet)) == 4 and not packet_found:
            print('packet', idx + 1)
            packet_found = True

        if len(set(queue_message)) == 14:
            print('message', idx + 1)
            break


if __name__ == '__main__':
    main()