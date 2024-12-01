def get_inputs(file):
    with open(file) as f:
        input = f.read()

    return input.strip("\n").split(",")


def hash(string) -> int:
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


def parse_input(input):
    if "-" in input:
        label = input[: input.index("-")]
        hash_val = hash(label)

        return ["-", hash_val, label]

    elif "=" in input:
        label, focal_length = input.split("=")
        hash_val = hash(label)

        return ["=", hash_val, label, focal_length]

    return [""]


def solve_part2(file):
    inputs = get_inputs(file)
    boxes = [[] for _ in range(256)]

    for input in inputs:
        parse_res = parse_input(input)

        operation = parse_res[0]

        if operation == "=":
            hash_val, label, focal_length = parse_res[1:]

            box = boxes[hash_val]

            label_exists = False
            for i, v in enumerate(box):
                v_label, _ = v.split(" ")

                if v_label == label:
                    box[i] = f"{label} {focal_length}"
                    label_exists = True

            if not label_exists:
                box.append(f"{label} {focal_length}")

        elif operation == "-":
            hash_val, label = parse_res[1:]

            box = boxes[hash_val]

            label_ind = -1
            for i, v in enumerate(box):
                v_label, _ = v.split(" ")

                if v_label == label:
                    label_ind = i

            if label_ind != -1:
                box.pop(label_ind)

    # get val

    focusing_power = 0
    for i, box in enumerate(boxes):
        for j, val in enumerate(box):
            _, focal_length = val.split(" ")

            focusing_power += (i + 1) * (j + 1) * int(focal_length)

    # print([box for box in boxes if box])
    print(focusing_power)


if __name__ == "__main__":
    import sys

    # solve_part1(sys.argv[1])
    solve_part2(sys.argv[1])

