def get_inputs(file):
    with open(file) as f:
        input = f.read()

    return input.strip("\n").split(",")


def hash(string):
    curr_val = 0
    for char in string:
        curr_val += ord(char)
        curr_val *= 17
        curr_val %= 256

    return curr_val


def solve_part1(file):
    inputs = get_inputs(file)

    hash_sum = 0
    for input in inputs:
        hash_val = hash(input)
        hash_sum += hash_val

    print(hash_sum)


if __name__ == "__main__":
    import sys

    solve_part1(sys.argv[1])
    # solve_part2(sys.argv[1])

