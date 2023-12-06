from collections import defaultdict
from pprint import pprint


def get_inputs(file):
    with open(file) as f:
        inputs = f.read().splitlines()

    return inputs


# Part 1
def parse_inputs(inputs):
    items = defaultdict(list)
    seeds = inputs[0]
    seeds = seeds[seeds.index(":") + 1 :].strip().split(" ")

    items["seeds"] = [int(i) for i in seeds]

    conversion_mode = None

    for input in inputs[1:]:
        # too cool for a hashmap
        if input == "seed-to-soil map:":
            conversion_mode = "seed-to-soil"
            continue

        elif input == "soil-to-fertilizer map:":
            conversion_mode = "soil-to-fertilizer"
            continue

        elif input == "fertilizer-to-water map:":
            conversion_mode = "fertilizer-to-water"
            continue

        elif input == "water-to-light map:":
            conversion_mode = "water-to-light"
            continue

        elif input == "light-to-temperature map:":
            conversion_mode = "light-to-temperature"
            continue

        elif input == "temperature-to-humidity map:":
            conversion_mode = "temperature-to-humidity"
            continue

        elif input == "humidity-to-location map:":
            conversion_mode = "humidity-to-location"
            continue

        elif input == "":
            continue

        items[conversion_mode].append([int(i) for i in input.split(" ")])

    return items


def convert_src_to_dst(src, mapping):
    dst = src
    for m in mapping:
        dst_start, src_start, length = m

        if src_start <= src <= (src_start + length - 1):
            diff = src - src_start
            dst = dst_start + diff

    return dst


def get_location(seed, mappings):
    soil = convert_src_to_dst(seed, mappings["seed-to-soil"])
    fertilizer = convert_src_to_dst(soil, mappings["soil-to-fertilizer"])
    water = convert_src_to_dst(fertilizer, mappings["fertilizer-to-water"])
    light = convert_src_to_dst(water, mappings["water-to-light"])
    temperature = convert_src_to_dst(light, mappings["light-to-temperature"])
    humidity = convert_src_to_dst(temperature, mappings["temperature-to-humidity"])
    location = convert_src_to_dst(humidity, mappings["humidity-to-location"])

    # print(f"{seed}->{soil}->{water}->{light}->{temperature}->{humidity}->{location}")

    return location


def solve_part1(file):
    """
    mapping format

    dst_start src_start length
    """

    inputs = get_inputs(file)
    items = parse_inputs(inputs)

    locations = []

    for seed in items["seeds"]:
        location = get_location(seed, items)
        locations.append(location)

    print(locations)
    print(min(locations))


def solve_part2(file):
    inputs = get_inputs(file)
    items = parse_inputs(inputs)

    min_location = float("inf")
    seeds = items["seeds"]
    for i in range(0, len(seeds), 2):
        starting_seed, num_seeds = seeds[i], seeds[i + 1]

        for seed in range(starting_seed, starting_seed + num_seeds):
            location = get_location(seed, items)
            min_location = min(min_location, location)
            print(location)

    print(min_location)
    return min_location


if __name__ == "__main__":
    import sys

    # solve_part1(sys.argv[1])
    solve_part2(sys.argv[1])
