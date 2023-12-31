dirs_map = {
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

vertical_pipes = {"|", "L" "J", "7", "F"}


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

    for dir_letter, dir in dirs_map.items():
        r_dir, c_dir = dir

        if (0 <= (r + r_dir) < len(matrix)) and (0 <= (c + c_dir) < len(matrix[0])):
            surrounding_pipe = matrix[r + r_dir][c + c_dir]
            can_connect = (
                surrounding_pipe in coming_from_map[opposite_dir_map[dir_letter]]
            )
            can_connect_list.append(can_connect)
        else:
            can_connect_list.append(False)

    return pipe_inference_map[tuple(can_connect_list)]


def bfs(S, matrix):
    largest_num_steps = 0
    queue = [(S, None, 0)]
    visited = set()

    while queue:
        curr_node, coming_from, num_step = queue.pop(0)
        r, c = curr_node

        if curr_node in visited:
            continue

        if (r < 0 or r >= len(matrix)) or (c < 0 or c >= len(matrix[0])):
            continue

        curr_pipe = matrix[r][c]
        if coming_from and (curr_pipe not in coming_from_map[coming_from]):
            continue

        if curr_pipe == "S":
            curr_pipe = infer_starting_pipe(curr_node, matrix)

        largest_num_steps = max(largest_num_steps, num_step)
        visited.add(curr_node)

        for dir in next_valid_dir[curr_pipe]:
            dir_r, dir_c = dirs_map[dir]
            new_node = (r + dir_r, c + dir_c)
            if new_node not in visited:
                queue.append((new_node, opposite_dir_map[dir], num_step + 1))

    print("largest num steps: ")
    print(largest_num_steps)

    return visited


def solve_part1(file):
    matrix = get_inputs(file)

    S = find_starting_pos(matrix)

    bfs(S, matrix)


def replace_S_with_pipe(S, starting_pipe, matrix):
    temp_row = matrix[S[0]]

    temp_row = [c for c in temp_row]
    temp_row[S[1]] = starting_pipe

    matrix[S[0]] = "".join(temp_row)

    return matrix


def solve_part2(file):
    """
    Solution is you have to horizontally scan the pipes, when encountering vertical pipes, you "switch modes"

    i.e.
    OOvIIIIvOO
    ..F----7..
    ..|....|..
    ..|....|..
    ..L----J..

    """

    matrix = get_inputs(file)
    S = find_starting_pos(matrix)
    starting_pipe = infer_starting_pipe(S, matrix)
    matrix = replace_S_with_pipe(S, starting_pipe, matrix)

    num_tiles_enclosed = 0
    modes = ["outside", "inside"]
    mode_ind = 0

    pipes = bfs(S, matrix)

    # horizontal scan
    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            curr_node = (r, c)
            curr_pipe = matrix[r][c]

            if (curr_pipe in vertical_pipes) and (curr_node in pipes):
                mode_ind = (mode_ind + 1) % len(modes)
                # print(f"encounered {curr_pipe}, switching mode to {modes[mode_ind]}")
                continue

            if (curr_node not in pipes) and modes[mode_ind] == "inside":
                # print(curr_node)
                num_tiles_enclosed += 1

    print(num_tiles_enclosed)


if __name__ == "__main__":
    import sys

    # solve_part1(sys.argv[1])
    solve_part2(sys.argv[1])
