dirs = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
}

opposite_dir_map = {"N": "S", "S": "N", "E": "W", "W": "E"}

next_valid_dir = {
    "|": ["N", "S"],
    "-": ["E", "W"],
    "L": ["N", "E"],
    "J": ["N", "W"],
    "7": ["S", "W"],
    "F": ["S", "E"],
}

coming_from_map = {
    "N": ["|", "L", "J"],  # coming from north, means traveling south
    "S": ["|", "7", "F"],  # traveling north
    "E": ["-", "L", "F"],  # traveling west
    "W": ["-", "7", "J"],  # traveling east
}

pipe_inference_map = {
    # (N S E W)
    (True, True, False, False): "|",
    (False, False, True, True): "-",
    (True, False, True, False): "L",
    (True, False, False, True): "J",
    (False, True, False, True): "7",
    (False, True, True, False): "F",
}


def get_inputs(file):
    with open(file) as f:
        inputs = f.read().splitlines()

    return inputs


def find_starting_pos(matrix):
    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            if matrix[r][c] == "S":
                return (r, c)

    return (-1, -1)


def infer_starting_pipe(S, matrix):
    r, c = S

    can_connect_list = []

    for dir_letter, dir in dirs.items():
        r_dir, c_dir = dir

        if (0 <= (r + r_dir) <= len(matrix)) and (0 <= (c + c_dir) <= len(matrix[0])):
            surrounding_pipe = matrix[r + r_dir][c + c_dir]
            can_connect = (
                surrounding_pipe in coming_from_map[opposite_dir_map[dir_letter]]
            )
            can_connect_list.append(can_connect)
        else:
            can_connect_list.append(False)

    return pipe_inference_map[tuple(can_connect_list)]


def solve_part1(file):
    matrix = get_inputs(file)

    S = find_starting_pos(matrix)
    starting_pipe = infer_starting_pipe(S, matrix)

    print(starting_pipe)


if __name__ == "__main__":
    import sys

    solve_part1(sys.argv[1])
    # solve_part2(sys.argv[1])
