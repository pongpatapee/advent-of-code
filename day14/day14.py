from collections import defaultdict
from pprint import pprint


def get_inputs(file):
    with open(file) as f:
        inputs = f.read().splitlines()

    return inputs


def get_rock_loc(matrix):
    round_rocks = []
    cube_rocks = []

    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            if matrix[r][c] == "O":
                round_rocks.append([r, c])
            elif matrix[r][c] == "#":
                cube_rocks.append([r, c])

    return round_rocks, cube_rocks


def push_rock_north(round_rocks, cube_rocks):
    # group by columns
    round_rocks_dict = defaultdict(list)
    cube_rocks_dict = defaultdict(list)

    for rock in round_rocks:
        r, c = rock
        round_rocks_dict[c].append([r, c])

    for rock in cube_rocks:
        r, c = rock
        cube_rocks_dict[c].append([r, c])

    # rows should already be sorted from the construction of get_rock_loc
    # pprint(round_rocks_dict)
    # pprint(cube_rocks_dict)

    for col in round_rocks_dict:
        curr_min = 0
        cube_ind = 0
        for i, pos in enumerate(round_rocks_dict[col]):
            r, c = pos

            # cube_row = cube_rocks_dict[col][cube_ind][0]
            while cube_ind < len(cube_rocks_dict[col]) and (
                r > cube_rocks_dict[col][cube_ind][0]
                or curr_min > cube_rocks_dict[col][cube_ind][0]
            ):
                cube_row = cube_rocks_dict[col][cube_ind][0]
                curr_min = max(curr_min, cube_row + 1)
                cube_ind += 1

            new_r = min(r, curr_min)
            round_rocks_dict[col][i] = [new_r, c]
            curr_min += 1

    # print("after")
    # pprint(round_rocks_dict)
    # pprint(cube_rocks_dict)
    return round_rocks_dict


def calc_total_load(round_rocks_dict, num_rows):
    total_load = 0
    for col in round_rocks_dict:
        for pos in round_rocks_dict[col]:
            r, c = pos

            total_load += num_rows - r

    return total_load


def solve_part1(file):
    inputs = get_inputs(file)
    round_rocks, cube_rocks = get_rock_loc(inputs)

    round_rocks_dict = push_rock_north(round_rocks, cube_rocks)
    total_load = calc_total_load(round_rocks_dict, len(inputs))

    print(total_load)


if __name__ == "__main__":
    import sys

    solve_part1(sys.argv[1])
    # solve_part2(sys.argv[1])

