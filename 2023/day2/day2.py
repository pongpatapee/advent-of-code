import re


def get_inputs(file):
    with open(file) as f:
        inputs = f.read().splitlines()

    return inputs


def parse_game_string(game_str):
    id_pattern = r"Game (\d+):"
    color_pattern = r"((\d+) (\w+),*)"

    match = re.match(id_pattern, game_str)
    id = match.group(1)
    game = {
        "id": int(id),
        "red": [],
        "green": [],
        "blue": [],
    }

    colon_ind = game_str.index(":")
    game_str = game_str[colon_ind + 1 :]
    cube_shows = game_str.split(";")

    for show in cube_shows:
        matches = re.findall(color_pattern, show)
        for match in matches:
            num = match[1]
            color = match[2]
            game[color].append(int(num))

    return game


def is_impossible(game, bag):
    for color in game:
        if color == "id":
            continue

        for num in game[color]:
            if num > bag[color]:
                return True

    return False


def solve_part1():
    bag = {"red": 12, "green": 13, "blue": 14}

    inputs = get_inputs("./inputs.txt")
    games = [parse_game_string(input) for input in inputs]

    id_sum = 0

    for game in games:
        if is_impossible(game, bag):
            continue

        id_sum += game["id"]

    return id_sum


def solve_part2():
    bag = {"red": 12, "green": 13, "blue": 14}

    inputs = get_inputs("./inputs.txt")
    games = [parse_game_string(input) for input in inputs]

    power_sum = 0
    for game in games:
        if game["red"]:
            min_red = max(game["red"])
        else:
            min_red = 0

        if game["green"]:
            min_green = max(game["green"])
        else:
            min_green = 0

        if game["blue"]:
            min_blue = max(game["blue"])
        else:
            min_blue = 0

        power = min_red * min_green * min_blue
        power_sum += power

    return power_sum


if __name__ == "__main__":
    print(solve_part2())
