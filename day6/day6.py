def get_inputs(file):
    with open(file) as f:
        inputs = f.read().splitlines()

    return inputs


def parse_inputs(inputs):
    times = inputs[0]
    distances = inputs[1]

    times = times[times.index(":") + 1 :].strip().split(" ")
    times = [int(t) for t in times if t != ""]

    distances = distances[distances.index(":") + 1 :].strip().split(" ")
    distances = [int(d) for d in distances if d != ""]

    print(times)
    print(distances)

    return times, distances


def num_way_beat_race(time, distance):
    # brute force cuz math is hard

    times_beaten = 0
    for t in range(time + 1):
        hold_button = t
        distance_travel = hold_button * (time - t)

        if distance_travel > distance:
            times_beaten += 1

    return times_beaten


def solve_part1(file):
    inputs = get_inputs(file)
    times, distances = parse_inputs(inputs)

    res = 1
    for time, distance in zip(times, distances):
        times_beaten = num_way_beat_race(time, distance)
        res *= times_beaten

    print(res)
    return res


def parse_inputs_part2(inputs):
    time = inputs[0]
    distance = inputs[1]

    time = time[time.index(":") + 1 :].strip()
    time = "".join([t for t in time if t.isdigit()])
    distance = distance[distance.index(":") + 1 :].strip()
    distance = "".join([d for d in distance if d.isdigit()])

    print(time, distance)

    return int(time), int(distance)


def solve_part2(file):
    inputs = get_inputs(file)
    time, distance = parse_inputs_part2(inputs)

    times_beaten = num_way_beat_race(time, distance)

    print(times_beaten)


if __name__ == "__main__":
    import sys

    # solve_part1(sys.argv[1])
    solve_part2(sys.argv[1])
