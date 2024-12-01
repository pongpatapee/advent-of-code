from pprint import pprint


def get_inputs(file):
    with open(file) as f:
        inputs = f.read().splitlines()

    return inputs


def parse_inputs(inputs):
    image = []

    for input in inputs:
        image.append([char for char in input])

    return image


def get_no_galaxy_rows(image):
    no_galaxy_rows = []

    for i, row in enumerate(image):
        if "#" not in row:
            no_galaxy_rows.append(i)

    return no_galaxy_rows


def get_no_galaxy_cols(image):
    no_galaxy_cols = []

    for c in range(len(image[0])):
        has_galaxy = False
        for r in range(len(image)):
            if image[r][c] == "#":
                has_galaxy = True

        if not has_galaxy:
            no_galaxy_cols.append(c)

    return no_galaxy_cols


def insert_row(image, row_ind):
    new_row = ["."] * len(image[0])
    image.insert(row_ind, new_row)

    return image


def insert_col(image, col_ind):
    for r in range(len(image)):
        row = image[r]
        row.insert(col_ind, ".")

    return image


def expand_galaxy(image):
    no_galaxy_rows = get_no_galaxy_rows(image)
    no_galaxy_cols = get_no_galaxy_cols(image)

    # print("inserting rows")
    # print(no_galaxy_rows)
    # print("inserting cols")
    # print(no_galaxy_cols)

    for i, row in enumerate(no_galaxy_rows):
        num_row_inserted = i + 1
        image = insert_row(image, row + num_row_inserted)

    for i, col in enumerate(no_galaxy_cols):
        num_row_inserted = i + 1
        image = insert_col(image, col + num_row_inserted)

    return image


def get_galaxy_inds(image):
    galaxy_inds = []
    for r in range(len(image)):
        for c in range(len(image[r])):
            if image[r][c] == "#":
                galaxy_inds.append([r, c])

    return galaxy_inds


def generate_pairs(galaxies):
    pairs = []
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            pairs.append([galaxies[i], galaxies[j]])

    return pairs


def calc_distance(node1, node2):
    # min distance is the taxi-cab distance because its a grid
    # since its just the L1 distance, the min distance = diffx + diffy

    distance = abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

    return distance


def solve_part1(file):
    inputs = get_inputs(file)
    image = parse_inputs(inputs)
    image = expand_galaxy(image)

    galaxy_inds = get_galaxy_inds(image)
    pairs = generate_pairs(galaxy_inds)

    total_distance = 0
    for pair in pairs:
        node1, node2 = pair
        distance = calc_distance(node1, node2)
        print(node1, node2, distance)
        total_distance += distance

    print(total_distance)


def expand_galaxy_from_inds(galaxy_inds, no_galaxy_rows, no_galaxy_cols, image):
    # no_galaxy_rows and no_galaxy_cols are naturally sorted from how they are constructed

    # -1 because we are replacing the empty space with the factor, not inserting
    expand_factor = 1_000_000 - 1

    no_row_ind = 0
    no_galaxy_rows.append(len(image))  # avoid no_row_ind out of bounds

    no_col_ind = 0
    no_galaxy_cols.append(len(image[0]))  # avoid no_col_ind out of bounds
    #
    # print(galaxy_inds)
    # print("before expansion")

    # exapand rows
    galaxy_inds.sort(key=lambda x: x[0])
    for i, galaxy in enumerate(galaxy_inds):
        r, c = galaxy

        # if no_row_ind < len(no_galaxy_rows) and (r > no_galaxy_rows[no_row_ind]):
        while r > no_galaxy_rows[no_row_ind]:
            no_row_ind += 1

        galaxy_inds[i] = [r + expand_factor * no_row_ind, c]

    # exapnd cols
    galaxy_inds.sort(key=lambda x: x[1])
    for i, galaxy in enumerate(galaxy_inds):
        r, c = galaxy

        while c > no_galaxy_cols[no_col_ind]:
            no_col_ind += 1

        galaxy_inds[i] = [r, c + expand_factor * no_col_ind]

    # print("after expansion")
    # galaxy_inds.sort(key=lambda x: x[0])
    # print(galaxy_inds)

    return galaxy_inds


def solve_part2(file):
    inputs = get_inputs(file)
    image = parse_inputs(inputs)

    galaxy_inds = get_galaxy_inds(image)  # galaxy_inds of unexpand galaxy

    no_galaxy_rows = get_no_galaxy_rows(image)
    no_galaxy_cols = get_no_galaxy_cols(image)
    # print("no_galaxy_rows")
    # print(no_galaxy_rows)
    # print("no_galaxy_cols")
    # print(no_galaxy_cols)

    galaxy_inds = expand_galaxy_from_inds(
        galaxy_inds, no_galaxy_rows, no_galaxy_cols, image
    )

    pairs = generate_pairs(galaxy_inds)

    total_distance = 0
    for pair in pairs:
        node1, node2 = pair
        distance = calc_distance(node1, node2)
        # print(node1, node2, distance)
        total_distance += distance

    print(total_distance)


if __name__ == "__main__":
    import sys

    # solve_part1(sys.argv[1])
    solve_part2(sys.argv[1])
