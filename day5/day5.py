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


def calc_overlap(src_start, src_length, dst_start, dst_length):
    a = src_start
    b = src_start + src_length - 1
    c = dst_start
    d = dst_start + dst_length - 1

    print(a, b, c, d)

    # a--------b
    #   c---d
    if a <= c and d <= b:
        return (d - c) + 1

    # a---b
    #   c---d
    elif a <= c and b <= d and c <= b:
        return (b - c) + 1

    #   a---b
    # c---d
    elif c <= a and d <= b and a <= d:
        return (d - a) + 1

    #   a---b
    # c--------d
    elif c <= a and b <= d:
        return (b - a) + 1

    return 0


def get_overlap_range(src_start, src_length, dst_start, dst_length):
    a = src_start
    b = src_start + src_length - 1
    c = dst_start
    d = dst_start + dst_length - 1

    # a--------b
    #   c---d
    if a <= c and d <= b:
        return (c, d)

    # a---b
    #   c---d
    elif a <= c and b <= d and b <= d:
        return (c, b)

    #   a---b
    # c---d
    elif c <= a and d <= b and a <= d:
        return (a, d)

    #   a---b
    # c--------d
    elif c <= a and b <= d:
        return (a, b)

    return None


def get_lowest_ranges(input_range, mappings):
    if input_range is None:
        min_dst = float("inf")
        min_dst_ind = None
        for i, m in enumerate(mappings):
            dst_start = m[0]
            min_dst = min(min_dst, dst_start)
            min_dst_ind = i

        dst, src, length = mappings[min_dst_ind]

        return src, length

    closest_range = None
    src_start, length = input_range
    max_over_lap = float("-inf")
    min_diff = float("inf")
    for m in mappings:
        m_dst, m_src, m_length = m

        overlap = calc_overlap(src_start, length, m_dst, m_length)
        if overlap == 0 and max_over_lap == float("-inf"):
            diff = abs(src_start - (m_dst + m_length - 1))
            if diff < min_diff:
                min_diff = diff
                closest_range = m_src, m_length

        elif overlap > max_over_lap:
            max_over_lap = overlap
            closest_range = m_src, m_length

    return closest_range


def solve_part2(file):
    inputs = get_inputs(file)
    items = parse_inputs(inputs)

    seeds = items["seeds"]
    seed_ranges = []
    for i in range(0, len(seeds), 2):
        starting_seed, num_seeds = seeds[i], seeds[i + 1]
        seed_ranges.append([starting_seed, num_seeds])

    # Going backwards None -> location -> humidity -> temperature -> light -> water -> fertilizer -> soil -> seed
    lowest_humidity_range = get_lowest_ranges(None, items["humidity-to-location"])
    lowest_temperature_range = get_lowest_ranges(
        lowest_humidity_range, items["temperature-to-humidity"]
    )
    lowest_light_range = get_lowest_ranges(
        lowest_temperature_range, items["light-to-temperature"]
    )
    lowest_water_range = get_lowest_ranges(lowest_light_range, items["water-to-light"])
    lowest_fertilizer_range = get_lowest_ranges(
        lowest_water_range, items["fertilizer-to-water"]
    )
    lowest_soil_range = get_lowest_ranges(
        lowest_fertilizer_range, items["soil-to-fertilizer"]
    )
    lowest_seed_range = get_lowest_ranges(lowest_soil_range, items["seed-to-soil"])

    print(lowest_humidity_range)
    print(lowest_temperature_range)
    print(lowest_light_range)
    print(lowest_water_range)
    print(lowest_fertilizer_range)
    print(lowest_soil_range)
    print(lowest_seed_range)

    max_over_lap = 0
    overlap_range = None
    for seed_range in seed_ranges:
        overlap = calc_overlap(*lowest_seed_range, *seed_range)
        print(overlap)
        if overlap > max_over_lap:
            max_over_lap = overlap
            overlap_range = get_overlap_range(*lowest_seed_range, *seed_range)

    # if overlap_range is None:
    #     return
    #
    print(overlap_range)
    lower_bound, upper_bound = overlap_range

    min_location = float("inf")
    for seed in range(lower_bound, upper_bound + 1):
        location = get_location(seed, items)
        # print(seed, location)
        min_location = min(location, min_location)

    ## test
    # location = get_location(70, items)
    # print(location)
    ## test

    # print(min_location)
    # return min_location


if __name__ == "__main__":
    import sys

    # solve_part1(sys.argv[1])
    solve_part2(sys.argv[1])
