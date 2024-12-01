import string


# Part 1
def get_inputs(file):
    with open(file) as f:
        lines = f.read().splitlines()

        return lines


def extract_calibration_part1(input_str):
    digits = [c for c in input_str if c in string.digits]
    first_last_digit = f"{digits[0]}{digits[-1]}"

    return int(first_last_digit)


def trebuchet_part1():
    inputs = get_inputs("./trebuchet_input.txt")
    calibration_vals = [extract_calibration_part1(input) for input in inputs]
    return sum(calibration_vals)


# Part 2

num_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}


def build_trie(words, vals):
    root = {}
    for i, word in enumerate(words):
        curr_dict = root
        for letter in word:
            if letter in curr_dict:
                curr_dict = curr_dict[letter]
            else:
                curr_dict[letter] = {}
                curr_dict = curr_dict[letter]

        curr_dict["_end_"] = vals[i]
    return root


def extract_calibration_part2_with_trie(num_str):
    digits = []
    num_trie = build_trie(list(num_map.keys()), list(num_map.values()))
    trie = num_trie

    i = 0
    while i < len(num_str):
        char = num_str[i]

        if char in string.digits:
            digits.append(char)
            i += 1
            continue

        # use trie
        if char in trie:
            trie = trie[char]

            if "_end_" in trie.keys():
                digits.append(trie["_end_"])
                trie = num_trie

        else:
            trie = num_trie
            if char in trie:
                trie = trie[char]

                if "_end_" in trie.keys():
                    digits.append(trie["_end_"])
                    trie = num_trie
        i += 1
    print(digits)
    first_last_digit = f"{digits[0]}{digits[-1]}"

    return int(first_last_digit)


num_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
}


def get_all_substring_ind(substring, string):
    inds = []

    i = 0
    while i < len(string):
        ind = string.find(substring, i)

        if ind == -1:
            break

        inds.append((ind, num_map[substring]))

        i = ind + len(substring)

    return inds


def extract_calibration_part2(num_str):
    digits = []

    # serach for all index of substrings
    for spell in num_map.keys():
        inds = get_all_substring_ind(spell, num_str)
        digits.extend(inds)

    digits.sort(key=lambda x: x[0])

    digits = [item[1] for item in digits]

    return int(f"{digits[0]}{digits[-1]}")


def trebuchet_part2():
    inputs = get_inputs("./trebuchet_input.txt")
    calibration_vals = [extract_calibration_part2(input) for input in inputs]
    # print(calibration_vals)
    return sum(calibration_vals)


if __name__ == "__main__":
    # print(trebuchet_part1())

    # trie = build_trie(list(num_map.keys()), list(num_map.values()))
    # pprint(trie)
    # digits = extract_calibration_part2("oneabctwofonce")
    # print(digits)

    print(trebuchet_part2())
