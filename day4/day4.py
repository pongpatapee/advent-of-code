from collections import defaultdict
from pprint import pprint


def get_inputs(file):
    with open(file) as f:
        inputs = f.read().splitlines()

    return inputs


def parse_input(input):
    card = input.split(":")
    winning_nums, card_nums = card[1].split("|")

    winning_nums = winning_nums.strip().split(" ")
    card_nums = card_nums.strip().split(" ")

    winning_nums = [num for num in winning_nums if num != ""]
    card_nums = [num for num in card_nums if num != ""]

    return winning_nums, card_nums


def solve_part1(file):
    inputs = get_inputs(file)

    total_points = 0
    for input in inputs:
        num_matches = 0

        winning_nums, card_nums = parse_input(input)
        winning_nums = set(winning_nums)

        for num in card_nums:
            if num in winning_nums:
                num_matches += 1

        if num_matches > 0:
            total_points += 2 ** (num_matches - 1)

    print(total_points)
    return total_points


def calc_num_matches(winning_nums, card_nums):
    winning_nums = set(winning_nums)
    num_matches = 0
    for num in card_nums:
        if num in winning_nums:
            num_matches += 1
            # print(f"matched: {num}, num_matches: {num_matches}")

    return num_matches


def solve_part2_brute_force(file):
    inputs = get_inputs(file)

    queue = [i + 1 for i in range(len(inputs))]

    instances = defaultdict(int)
    for num in queue:
        instances[num] += 1

    while len(queue) > 0:
        index = queue.pop(0) - 1

        input = inputs[index]
        winning_nums, card_nums = parse_input(input)

        num_matches = calc_num_matches(winning_nums, card_nums)

        for i in range(1, num_matches + 1):
            new_scratch_card = (index + 1) + i

            queue.append(new_scratch_card)
            instances[new_scratch_card] += 1

    #     print(
    #         f"num_matches for {num_matches} for curr card {index + 1}, length of queue: {len(queue)}, curr num cards: {sum(instances.values())}"
    #     )
    #
    # print(instances)
    # print(sum(instances.values()))


def build_graph(inputs):
    graph = {}

    for i, input in enumerate(inputs):
        card_num = i + 1
        winning_nums, card_nums = parse_input(input)
        num_matches = calc_num_matches(winning_nums, card_nums)

        graph[card_num] = [card_num + j + 1 for j in range(num_matches)]

    return graph


def traverse_graph(graph, node, mem, cache_hits):
    num_nodes = 1
    for child in graph[node]:
        if child in mem:
            num_nodes += mem[child]
            cache_hits[0] += 1
        else:
            num_child_nodes = traverse_graph(graph, child, mem, cache_hits)
            num_nodes += num_child_nodes
            mem[child] = num_child_nodes

    return num_nodes


def solve_part2_memoized(file):
    inputs = get_inputs(file)
    graph = build_graph(inputs)

    mem = {}

    total_cards = 0
    cache_hits = [0]  # for funsies

    for card_num in range(1, len(inputs) + 1):
        if card_num in mem:
            num_nodes = mem[card_num]
        else:
            num_nodes = traverse_graph(graph, card_num, mem, cache_hits)

        total_cards += num_nodes

    print(f"cache hits: {cache_hits[0]}")
    print("ans:")
    print(total_cards)
    return total_cards


if __name__ == "__main__":
    import sys

    # solve_part1(sys.argv[1])
    solve_part2_memoized(sys.argv[1])

    # part 2 ans: 13080971
    #
    #
    #
    """
    # Cached vs no cached performance

    ❮ time python day4.py input.txt
    cache hits: 834
    ans:
    13080971
    python day4.py input.txt  0.02s user 0.00s system 97% cpu 0.024 total

    advent-of-code-2023/day4 on  main [?] via 🐍 v3.11.5
    ❮ time python day4.py input.txt
    cache hits: 0
    ans:
    13080971
    python day4.py input.txt  1.13s user 0.01s system 99% cpu 1.135 total
    """
