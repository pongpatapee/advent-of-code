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


def convert_start_length_to_interval(start, length):
    return start, (start + length - 1)


def get_overlap_range(src_start, src_end, dst_start, dst_end):
    a = src_start
    b = src_end
    c = dst_start
    d = dst_end

    # a--------b
    #   c---d
    if a <= c and d <= b:
        return (c, d)

    # a---b
    #   c---d
    elif a <= c and c <= b and b <= d:
        return (c, b)

    #   a---b
    # c---d
    elif c <= a and a <= d and d <= b:
        return (a, d)

    #   a---b
    # c--------d
    elif c <= a and b <= d:
        return (a, b)

    return None


def clean_intervals(intervals):
    intervals = [[start, end] for start, end in intervals if start <= end]

    return sorted(intervals, key=lambda x: x[0])


def merge_intervals(intervals):
    merge_intervals = [intervals.pop(0)]

    for start, end in intervals:
        p_start, p_end = merge_intervals[-1]

        if p_start <= start <= p_end:
            start = min(start, p_start)
            end = max(end, p_end)
            merge_intervals[-1] = [start, end]
        else:
            merge_intervals.append([start, end])

    return merge_intervals


def get_non_overlaps(curr_interval, overlaps):
    if not overlaps:
        return [curr_interval]

    curr_start, curr_end = curr_interval

    # create overlap set
    overlaps_set = set([tuple(interval) for interval in overlaps])

    overlaps.sort(key=lambda x: x[0])

    non_overlaps = []

    # start of curr_interval to beginning of overlap
    overlap_start = overlaps[0][0]
    if abs(curr_start - overlap_start) > 0:
        non_overlap = [curr_start, overlap_start - 1]
        non_overlaps.append(non_overlap)

    for i in range(len(overlaps) - 1):
        overlap_start, overlap_end = overlaps[i]
        next_overlap_start, next_overlap_end = overlaps[i + 1]

        if abs(overlap_end - next_overlap_start) > 1:
            non_overlap = [overlap_end + 1, next_overlap_start - 1]

            if tuple(non_overlaps) not in overlaps_set:
                non_overlaps.append(non_overlap)

    # end of overlap to end of interval
    overlap_end = overlaps[-1][1]
    if abs(overlap_end - curr_end) > 0:
        non_overlap = [overlap_end + 1, curr_end]
        non_overlaps.append(non_overlap)

    return non_overlaps


def apply_transformations(overlaps, transformations):
    transformed = []
    for overlap, transformation in zip(overlaps, transformations):
        start, end = overlap
        new_start, new_end = start + transformation, end + transformation
        transformed.append([new_start, new_end])

    return transformed


def get_transformed_intervals(curr_intervals, mappings):
    sorted_mapping = sorted(mappings, key=lambda x: x[1])
    transformed_intervals = []

    for curr_start, curr_end in curr_intervals:
        map_start = sorted_mapping[0][1]
        map_end = sorted_mapping[-1][1] + sorted_mapping[-1][2] - 1
        if curr_end < map_start or curr_start > map_end:
            transformed_intervals.append([curr_start, curr_end])
            continue

        overlaps = []
        transformations = []
        for m in sorted_mapping:
            m_dst_start, m_src_start, m_length = m
            m_src_end = m_src_start + m_length - 1

            overlap = get_overlap_range(curr_start, curr_end, m_src_start, m_src_end)

            if not overlap:
                continue

            overlaps.append(overlap)
            transformations.append(m_dst_start - m_src_start)

        non_overlap = get_non_overlaps([curr_start, curr_end], overlaps)

        transformed_intervals.extend(apply_transformations(overlaps, transformations))
        transformed_intervals.extend(non_overlap)

    transformed_intervals = clean_intervals(transformed_intervals)
    transformed_intervals = merge_intervals(transformed_intervals)
    # print(curr_intervals)
    # print([[m[0], m[1], m[1] + m[2] - 1, m[0] - m[1]] for m in sorted_mapping])
    # print(transformed_intervals)
    return transformed_intervals


def solve_part2(file):
    inputs = get_inputs(file)
    items = parse_inputs(inputs)

    seeds = items["seeds"]
    seed_intervals = []
    for i in range(0, len(seeds), 2):
        start, end = convert_start_length_to_interval(seeds[i], seeds[i + 1])
        seed_intervals.append([start, end])

    mappings = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]

    curr_intervals = sorted(seed_intervals, key=lambda x: x[0])
    for mapping in mappings:
        curr_intervals = get_transformed_intervals(curr_intervals, items[mapping])

    print("min_loc")
    print(min(curr_intervals, key=lambda x: x[0]))


if __name__ == "__main__":
    import sys

    # solve_part1(sys.argv[1])
    solve_part2(sys.argv[1])
