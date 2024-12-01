import re


def parse_game_string(game_str):
    id_pattern = r"Game (\d+):"
    color_pattern = r"((\d+) (\w+),*)"

    match = re.match(id_pattern, game_str)
    id = match.group(1)
    game = {
        "id": id,
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
            game[color].append(num)

    return game


string = "Game 100: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
print(parse_game_string(string))
