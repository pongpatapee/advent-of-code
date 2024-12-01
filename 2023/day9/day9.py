def get_inputs(file):
    with open(file) as f:
        inputs = f.read().splitlines()

    return inputs


def parse_inputs(inputs):
    parsed_inputs = []
    for input in inputs:
        input = input.split(" ")
        input = [int(i) for i in input]
        parsed_inputs.append(input)

    return parsed_inputs


def is_all_zeros(arr):
    for i in arr:
        if i != 0:
            return False

    return True


def extrapolate_history(history):
    diffs = [history]
    stack = [history[-1]]

    while not is_all_zeros(diffs[-1]):
        new_diff = []
        curr_hist = diffs[-1]
        for i in range(len(curr_hist) - 1):
            new_diff.append(curr_hist[i + 1] - curr_hist[i])

        stack.append(new_diff[-1])
        diffs.append(new_diff)

    # extrapolation part
    prev = stack.pop()  # always going to be 0
    while stack:
        curr = stack.pop()
        extrap = curr + prev
        prev = extrap

    return prev


def solve_part1(file):
    inputs = get_inputs(file)
    histories = parse_inputs(inputs)

    # extrapolate_history(histories[0])

    extrap_sum = 0
    for history in histories:
        extrap_sum += extrapolate_history(history)

    print(extrap_sum)


def extrapolate_history_backward(history):
    diffs = [history]
    stack = [history[0]]

    while not is_all_zeros(diffs[-1]):
        new_diff = []
        curr_hist = diffs[-1]
        for i in range(len(curr_hist) - 1):
            new_diff.append(curr_hist[i + 1] - curr_hist[i])

        stack.append(new_diff[0])
        diffs.append(new_diff)

    # extrapolation part
    prev = stack.pop()  # always going to be 0
    while stack:
        curr = stack.pop()
        extrap = curr - prev
        prev = extrap

    return prev


def solve_part2(file):
    inputs = get_inputs(file)
    histories = parse_inputs(inputs)

    extrap_sum = 0
    for history in histories[::-1]:
        extrap_sum += extrapolate_history_backward(history)

    print(extrap_sum)


if __name__ == "__main__":
    import sys

    # solve_part1(sys.argv[1])
    solve_part2(sys.argv[1])
