from collections import defaultdict
from functools import cmp_to_key
from pprint import pprint

CARD_VAL = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "1": 1,
}

CARD_VAL_PART_2 = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}

# Higher num = higher rank
TYPE_RANKING = {
    "5kind": 7,
    "4kind": 6,
    "fullhouse": 5,
    "3kind": 4,
    "2pair": 3,
    "1pair": 2,
    "highcard": 1,
}


def get_inputs(file):
    with open(file) as f:
        inputs = f.read().splitlines()

    return inputs


def parse_inputs(inputs):
    hand_bid_map = {}
    for i in range(len(inputs)):
        hand, bid = inputs[i].split(" ")
        hand_bid_map[hand] = int(bid)

    return hand_bid_map


def get_hand_type(hand):
    freq = defaultdict(int)
    for card in hand:
        freq[card] += 1

    sorted_hand = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    most_freq = sorted_hand[0][1]

    if most_freq == 5:
        return "5kind"
    elif most_freq == 4:
        return "4kind"
    elif most_freq == 3:
        second_freq = sorted_hand[1][1]
        if second_freq == 2:
            return "fullhouse"

        return "3kind"

    elif most_freq == 2:
        second_freq = sorted_hand[1][1]
        if second_freq == 2:
            return "2pair"

        return "1pair"

    return "highcard"


def compare_hands(hand1, hand2):
    hand1_type = get_hand_type(hand1)
    hand2_type = get_hand_type(hand2)

    if TYPE_RANKING[hand1_type] < TYPE_RANKING[hand2_type]:
        return -1
    if TYPE_RANKING[hand1_type] > TYPE_RANKING[hand2_type]:
        return 1

    else:  # same hand type
        i = 0
        while i < len(hand1) and (hand1[i] == hand2[i]):
            i += 1  # loop until no duplicate

        if i < len(hand1):
            if CARD_VAL[hand1[i]] < CARD_VAL[hand2[i]]:
                return -1
            if CARD_VAL[hand1[i]] > CARD_VAL[hand2[i]]:
                return 1

    return 0


def solve_part1(file):
    inputs = get_inputs(file)
    hand_bid_map = parse_inputs(inputs)

    hands = list(hand_bid_map.keys())
    hands.sort(key=cmp_to_key(compare_hands))

    total_winnings = 0
    for i, hand in enumerate(hands):
        total_winnings += (i + 1) * hand_bid_map[hand]

    print(total_winnings)


def get_hand_type_part2(hand):
    freq = defaultdict(int)
    for card in hand:
        freq[card] += 1

    sorted_hand = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    # Edge case (JJJJJ)
    if freq["J"] == 5:
        return "5kind"

    # Get most freq item that isn't J
    most_freq_ind = 0
    most_freq_hand = sorted_hand[most_freq_ind][0]
    most_freq = sorted_hand[most_freq_ind][1]

    if most_freq_hand == "J":
        most_freq_ind += 1
        most_freq_hand = sorted_hand[most_freq_ind][0]
        most_freq = sorted_hand[most_freq_ind][1]

    most_freq += freq["J"]  # add most freq card (that isn't J) with freq of J

    if most_freq == 5:
        return "5kind"
    elif most_freq == 4:
        return "4kind"
    elif most_freq == 3:
        second_freq = sorted_hand[most_freq_ind + 1][1]
        if second_freq == 2:
            return "fullhouse"

        return "3kind"

    elif most_freq == 2:
        second_freq = sorted_hand[most_freq_ind + 1][1]
        if second_freq == 2:
            return "2pair"

        return "1pair"

    return "highcard"


def compare_hands_part2(hand1, hand2):
    hand1_type = get_hand_type_part2(hand1)
    hand2_type = get_hand_type_part2(hand2)

    if TYPE_RANKING[hand1_type] < TYPE_RANKING[hand2_type]:
        return -1
    if TYPE_RANKING[hand1_type] > TYPE_RANKING[hand2_type]:
        return 1

    else:  # same hand type
        i = 0
        while i < len(hand1) and (hand1[i] == hand2[i]):
            i += 1  # loop until no duplicate

        if i < len(hand1):
            if CARD_VAL_PART_2[hand1[i]] < CARD_VAL_PART_2[hand2[i]]:
                return -1
            if CARD_VAL_PART_2[hand1[i]] > CARD_VAL_PART_2[hand2[i]]:
                return 1

    return 0


def solve_part2(file):
    inputs = get_inputs(file)
    hand_bid_map = parse_inputs(inputs)

    hands = list(hand_bid_map.keys())
    hands.sort(key=cmp_to_key(compare_hands_part2))

    total_winnings = 0
    for i, hand in enumerate(hands):
        print(hand, get_hand_type_part2(hand))
        total_winnings += (i + 1) * hand_bid_map[hand]

    print(total_winnings)


if __name__ == "__main__":
    import sys

    solve_part1(sys.argv[1])
    solve_part2(sys.argv[1])

    # part 1
    # 246409899

    # part 2
    # ans too low: 244683849
    # also wrong: 245383453
    # Final ans: 244848487
