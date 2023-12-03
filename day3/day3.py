from pprint import pprint
import numpy as np
from collections import defaultdict


def get_input(file):
    with open(file) as f:
        inputs = f.read().splitlines()

    return inputs


def print_mat(mat):
    for row in mat:
        frmt = "{:^5}" * len(row)
        print(frmt.format(*row))


def parse_num_and_space(input):
    output = []

    num_str = ""
    for n in input:
        if not n.isdigit():
            if num_str:
                # append number for x

                while "x" in output:
                    x_ind = output.index("x")
                    output[x_ind] = num_str

                num_str = ""

            output.append(n)

        else:
            output.append("x")  # mark spot where I should place numbers
            num_str += n

    return output


def is_symbol(char):
    if not char.isdigit() and char != ".":
        return True

    return False


def has_adjacent_symbol(num_ind, matrix):
    # num_ind (r, c)

    r, c = num_ind
    row_length = len(matrix)
    col_length = len(matrix[0])

    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP_LEFT = tuple(map(sum, zip(UP, LEFT)))
    UP_RIGHT = tuple(map(sum, zip(UP, RIGHT)))
    DOWN_LEFT = tuple(map(sum, zip(DOWN, LEFT)))
    DOWN_RIGHT = tuple(map(sum, zip(DOWN, RIGHT)))

    dirs = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

    for dir in dirs:
        rd, cd = dir

        # print("#########")
        # print(f"curr ind: {(r, c)}")
        # print(f"curr dir: {(rd, cd)}")
        # print("#########")

        if (
            (0 <= (r + rd) < row_length)
            and (0 <= (c + cd) < col_length)
            and is_symbol(matrix[r + rd][c + cd])
        ):
            return True

    return False


def solve_part1(file_input):
    inputs = get_input(file_input)
    parsed_inputs = [parse_num_and_space(input) for input in inputs]

    # get number bounds
    num_bounds = defaultdict(list)
    for i, row in enumerate(parsed_inputs):
        for j, col in enumerate(row):
            if col.isdigit():
                num_bounds[col].append((i, j))

    res = {}

    for num in num_bounds.keys():
        res[num] = False
        for ind in num_bounds[num]:
            if has_adjacent_symbol(ind, parsed_inputs):
                res[num] = True

    final_sum = 0
    for num in res:
        if res[num]:
            final_sum += int(num)

    pprint(num_bounds)
    pprint(res)
    print(final_sum)
    return final_sum


if __name__ == "__main__":
    solve_part1("./input.txt")
