def main():
    with open('../data/day2/rock_paper_scissors.txt', 'r') as file:
        lines = file.readlines()

    scores = []
    second_scores = []
    for line in lines:
        round_score = 0
        second_round_score = 0
        opponent, my = line.split()

        match opponent:
            case 'A':
                opp_num = 1
            case 'B':
                opp_num = 2
            case 'C':
                opp_num = 3
            case _:
                raise Exception('Case fallthrough!')

        win_map = {1: 2, 2: 3, 3: 1}
        loss_map = {1: 3, 2: 1, 3: 2}

        # handle the score for the selection
        match my:
            case 'X':
                round_score += 1
                my_num = 1
                second_round_score += loss_map[opp_num]
            case 'Y':
                round_score += 2
                my_num = 2
                second_round_score += 3 + opp_num
            case 'Z':
                round_score += 3
                my_num = 3
                second_round_score += 6 + win_map[opp_num]
            case _:
                raise Exception('Case fallthrough!')

        # determine if you won, tied or lost
        if opp_num - my_num == 0:
            # draw 3 cases
            round_score += 3
        elif opp_num - my_num == -1:
            # i win 2 cases
            round_score += 6
        elif opp_num - my_num == -2:
            # I lose 1 case
            pass
        elif opp_num - my_num == 1:
            # I lose 2 cases
            pass
        elif opp_num - my_num == 2:
            # I win 1 case:
            round_score += 6

        scores.append(round_score)
        second_scores.append(second_round_score)

    print(sum(scores))
    print(sum(second_scores))


if __name__ == '__main__':
    main()
