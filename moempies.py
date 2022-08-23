import random
import numpy as np
from collections import Counter


def name_midpoints(names):
    midpoints = []
    odd_even = []

    for name in names:
        num_chars = len(name)
        if num_chars % 2 == 0:
            odd_even.append(0)
            midpoints.append(int((num_chars)/2))
        else:
            odd_even.append(1)
            midpoints.append(int((num_chars + 1)/2))

    return midpoints, odd_even


def print_score(midpoints, odd_even, scores):
    formatted_score = ""
    for (i, (midpoint, (odd_even, score))) in enumerate(zip(midpoints,
                                                           zip(odd_even,
                                                               scores))):
        score = str(score)
        score_len = len(score)
        if score_len % 2 == 0:
            pre_adjustment = int((score_len - 2)/2)
            post_adjustment = int((score_len - 1)/2)
        else:
            pre_adjustment = int((score_len - 1)/2)
            post_adjustment = int((score_len - 1)/2)

        if odd_even == 1:
            end_space = " " * (midpoint - post_adjustment)
        else:
            end_space = " " * (midpoint - post_adjustment) + " "

        if i == 0:
            formatted_score += ("|" + " " * (midpoint-pre_adjustment) + score +
                                end_space + "|")
        else:
            formatted_score += (" " * (midpoint-pre_adjustment) + score +
                                end_space + "|")

    return formatted_score


def score_function(dice_num, occurrences):
    # todo: three of a kind
    score = 0

    if sorted(dice_num) == list(range(1, 7)):
        score = 3550

    elif (dice_num == 6) and (n == 2 for n in occurrences):
        # update
        score = 500
    else:
        for n, m in zip(occurrences, dice_num):
            if n >= 3:
                score += m * 10 * 10**(1+np.floor(abs(m-7)/6)) * 2**(n-3)
            elif m == 1:
                score += n * 100
            elif m == 5:
                score += n * 50

    return score


def player_turn(score, minimum_bank, num_dice=6):
    dice_nums, occurrences = roll_dice(num_dice)
    dice_score = score_function(dice_nums, occurrences)

    if dice_score == 0:
        print("Moempies!")
        return 0
    else:
        score += dice_score

    player_choice = "no"

    if score >= minimum_bank:
        print(f"Score: {score}")
        player_choice = str.lower(input("Do you want to bank? "
                                        "\nType yes or no: "))

    if player_choice == "yes":
            return score
    else:
        print(f"Score: {score}")
        # todo: implement keeping score
        if score < minimum_bank:
            print(f"Score is less than minimum bank")

        hold = int(input("How much do you want to hold? "))
        num_dice = int(input("How many dice are left? "))

        # todo: implement max score to hold
        score = hold

        return player_turn(score, minimum_bank, num_dice)


def roll_dice(num_dice):
    dice_roll = random.choices(range(1, 6), k=num_dice)

    print(dice_roll)

    counter = Counter(dice_roll)
    dice_nums = [key for key in counter]
    occurrences = [counter[key] for key in counter]

    return dice_nums, occurrences


if __name__ == "__main__":
    s = (
        "███╗   ███╗ ██████╗ ███████╗███╗   ███╗██████╗ ██╗████████╗███████╗"
        "\n████╗ ████║██╔═══██╗██╔════╝████╗ ████║██╔══██╗██║╚══██╔══╝██╔════╝"
        "\n██╔████╔██║██║   ██║█████╗  ██╔████╔██║██████╔╝██║   ██║   ███████╗"
        "\n██║╚██╔╝██║██║   ██║██╔══╝  ██║╚██╔╝██║██╔═══╝ ██║   ██║   ╚════██║"
        "\n██║ ╚═╝ ██║╚██████╔╝███████╗██║ ╚═╝ ██║██║     ██║   ██║   ███████║"
        "\n╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝   ╚═╝   ╚══════╝"
    )

    print(s)

    num_players = int(input("\n\nHow many people are playing: "))
    print("Please enter the player names")
    players = []
    player_scores = [0] * num_players
    for player in range(num_players):
        player_name = str(input(f"Player {player+1}: "))
        players.append(player_name)

    state = "start"

    print("\nGet ready for moempies!\n")
    formatted_header = "| " + " | ".join(players) + " |"
    formatted_header = ("-" * len(formatted_header) + "\n" +
                        formatted_header + "\n" +
                        "-" * len(formatted_header))

    midpoints, odd_even = name_midpoints(players)

    formatted_score = print_score(midpoints, odd_even, player_scores) + "\n"

    round_num = 1

    while state != "quit" and int(max(player_scores)) < 10000:
        print(f"\nRound: {round_num}\n" + formatted_header)
        print(formatted_score)

        minimum_bank = 350

        if max(player_scores) > 5000:
            minimum_bank = 550
            print("\nMinimum bank is now 550")

        for i in range(num_players):
            state = str(input(f"\n{players[i]} dice"))
            print("Rolling...\n")

            score = player_turn(0, minimum_bank)

            player_scores[i] += score

        formatted_score = (formatted_score +
                           print_score(midpoints, odd_even, player_scores)
                           + "\n")

        round_num += 1
