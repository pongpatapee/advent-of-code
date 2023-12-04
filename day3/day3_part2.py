from collections import defaultdict


def add_tuples(a, b):
    return tuple(map(sum, zip(a, b)))


def get_input(file):
    with open(file) as f:
        inputs = f.read().splitlines()

    return inputs


def print_mat(mat):
    for row in mat:
        frmt = "{:^5}" * len(row)
        print(frmt.format(*row))


def print_mapping(num_map, res):
    for i, n in enumerate(num_map):
        print(f"{i} -> {n}: {res[str(i)]}")


def parse_num_and_space(input, num_id):
    output = []

    num_str = ""
    for n in input:
        if not n.isdigit():
            if num_str:
                # append number for x
                num_id.append(num_str)

                while "x" in output:
                    x_ind = output.index("x")
                    output[x_ind] = str(len(num_id) - 1)

                num_str = ""

            output.append(n)

        else:
            output.append("x")  # mark spot where I should place numbers
            num_str += n

    if num_str:
        # append number for x
        num_id.append(num_str)

        while "x" in output:
            x_ind = output.index("x")
            output[x_ind] = str(len(num_id) - 1)

        num_str = ""

    return output, num_id


def get_adjacent_gear_parts(gear_ind, num_bounds):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP_LEFT = add_tuples(UP, LEFT)
    UP_RIGHT = add_tuples(UP, RIGHT)
    DOWN_LEFT = add_tuples(DOWN, LEFT)
    DOWN_RIGHT = add_tuples(DOWN, RIGHT)

    dirs = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

    adjacent_parts = []

    for num_id in num_bounds:
        for dir in dirs:
            if add_tuples(gear_ind, dir) in num_bounds[num_id]:
                if num_id in adjacent_parts:
                    continue

                adjacent_parts.append(num_id)

    return adjacent_parts


def get_gear_ratios(num_bounds, matrix, num_ids):
    gear_ratio = 0

    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            if matrix[r][c] == "*":
                adjacent_parts = get_adjacent_gear_parts((r, c), num_bounds)

                # print([num_ids[int(n)] for n in adjacent_parts])

                if len(adjacent_parts) == 2:
                    num1 = int(num_ids[int(adjacent_parts[0])])
                    num2 = int(num_ids[int(adjacent_parts[1])])
                    gear_ratio += num1 * num2

    return gear_ratio


def get_num_bound_indicies(parsed_inputs):
    num_bounds = defaultdict(list)
    for i, row in enumerate(parsed_inputs):
        for j, col in enumerate(row):
            if col.isdigit():
                num_bounds[col].append((i, j))

    return num_bounds


def solve_part2(file_input):
    inputs = get_input(file_input)

    num_ids = []

    inputs = get_input(file_input)
    parsed_inputs = [parse_num_and_space(input, num_ids) for input in inputs]
    parsed_inputs = [parsed_input[0] for parsed_input in parsed_inputs]

    num_bounds = get_num_bound_indicies(parsed_inputs)

    gear_ratio_total = get_gear_ratios(num_bounds, parsed_inputs, num_ids)

    print(gear_ratio_total)
    return gear_ratio_total


if __name__ == "__main__":
    import sys

    solve_part2(sys.argv[1])
