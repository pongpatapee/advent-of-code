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


def get_overlap_range(src_start, src_length, dst_start, dst_length):
    a = src_start
    b = src_start + src_length - 1
    c = dst_start
    d = dst_start + dst_length - 1

    # a--------b
    #   c---d
    if a <= c and d <= b:
        # return [
        #     (c, d),
        #     (a, c),
        #     (d, b),
        # ]  # (c, d) = range in transformation, (a, c), (d, b) = range out of transformation
        return (c, d)

    # a---b
    #   c---d
    elif a <= c and c <= b and b <= d:
        # return [(c, b), (a, c)]  # same logic as above
        return (c, b)

    #   a---b
    # c---d
    elif c <= a and a <= d and d <= b:
        # return [(a, d), (d, b)]
        return (a, d)

    #   a---b
    # c--------d
    elif c <= a and b <= d:
        # return [(a, b)]
        return (a, b)

    # return [None, (a, b)]
    return None


def get_non_overlap_ranges(curr_range, new_ranges):
    curr_start, curr_length = curr_range

    total_non_overlap = None

    for new_range in new_ranges:
        new_start, new_length = new_range

        overlap = get_overlap_range(curr_start, curr_length, new_start, new_length)

        if overlap:
            overlap_start, overlap_end = overlap
            overlap_length = overlap_end - overlap_start + 1

            if overlap_length == 0:
                continue

            if overlap_start == curr_start:
                non_overlap_start = overlap_end + 1
                non_overlap_length = curr_length - overlap_length
                non_overlap_end = non_overlap_start + non_overlap_length - 1

            else:
                non_overlap_start = curr_start
                non_overlap_length = curr_length - overlap_length
                non_overlap_end = non_overlap_start + non_overlap_length - 1

            if total_non_overlap and non_overlap_length > 0:
                temp = get_overlap_range(
                    total_non_overlap[0],
                    total_non_overlap[1],
                    non_overlap_start,
                    non_overlap_length,
                )

                if temp:
                    start, end = temp
                    total_non_overlap = (start, start + end - 1)

            else:
                total_non_overlap = (non_overlap_start, non_overlap_length)

    return total_non_overlap


def apply_transformation(new_ranges, transformations):
    transformed_ranges = []
    for i in range(len(new_ranges)):
        transformed_ranges.append(
            (new_ranges[i][0] + transformations[i], new_ranges[i][1])
        )

    return transformed_ranges


def get_transformed_ranges(curr_ranges, mappings):
    num_ranges = len(curr_ranges)
    transformed_ranges = []

    for i in range(num_ranges):
        curr_range = curr_ranges.pop(0)
        new_ranges = []
        transformations = []
        for map_range in mappings:
            m_dst_start, m_src_start, m_length = map_range
            curr_start, curr_length = curr_range
            overlap = get_overlap_range(curr_start, curr_length, m_src_start, m_length)

            # print(
            #     f"curr range: {curr_range}, curr_map: {map_range}, overlap: {overlap}"
            # )

            if overlap is not None:
                lower_bound, upper_bound = overlap
                length = upper_bound - lower_bound + 1

                # Transform
                transformations.append(m_dst_start - m_src_start)
                new_ranges.append((lower_bound, length))

        if len(new_ranges) == 0:  # no overlap in any mapping found
            new_ranges = [curr_range]  # then put back current range
            transformations = [0]

        non_overlap_range = get_non_overlap_ranges(curr_range, new_ranges)
        print(
            f"curr range: {curr_range}, new_ranges: {new_ranges}, non-overlap: {non_overlap_range}"
        )
        new_ranges = apply_transformation(new_ranges, transformations)

        transformed_ranges.extend(new_ranges)
        if non_overlap_range is not None and non_overlap_range[1] > 0:
            transformed_ranges.append(non_overlap_range)

    print(transformed_ranges)
    return transformed_ranges


def solve_part2(file):
    inputs = get_inputs(file)
    items = parse_inputs(inputs)

    seeds = items["seeds"]
    seed_ranges = []
    for i in range(0, len(seeds), 2):
        starting_seed, num_seeds = seeds[i], seeds[i + 1]
        seed_ranges.append((starting_seed, num_seeds))

    # print(seed_ranges)
    print("current mapping: seed->soil")
    soil_ranges = get_transformed_ranges(seed_ranges, items["seed-to-soil"])
    print("current mapping: soil->fert")
    fertilizer_ranges = get_transformed_ranges(soil_ranges, items["soil-to-fertilizer"])
    print("current mapping: fert->water")
    water_ranges = get_transformed_ranges(
        fertilizer_ranges, items["fertilizer-to-water"]
    )
    print("current mapping: water->light")
    light_ranges = get_transformed_ranges(water_ranges, items["water-to-light"])
    print("current mapping: light->temp")
    temperature_ranges = get_transformed_ranges(
        light_ranges, items["light-to-temperature"]
    )
    print("current mapping: temp->humidity")
    humidity_ranges = get_transformed_ranges(
        temperature_ranges, items["temperature-to-humidity"]
    )
    print("current mapping: humidity->loc")
    location_ranges = get_transformed_ranges(
        humidity_ranges, items["humidity-to-location"]
    )

    print(location_ranges)

    min_loc = min(location_ranges, key=lambda x: x[0])
    print(min_loc)


if __name__ == "__main__":
    import sys

    # solve_part1(sys.argv[1])
    solve_part2(sys.argv[1])
