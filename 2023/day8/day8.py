dir_map = {"L": 0, "R": 1}


def get_inputs(file):
    with open(file) as f:
        inputs = f.read().splitlines()

    return inputs


def parse_node_input(node_input):
    node_len = 3

    nodes = []

    i = 0
    while i < len(node_input):
        if node_input[i].isalpha() or node_input[i].isdigit():
            nodes.append(node_input[i : i + node_len])
            i += node_len
            continue

        i += 1

    return nodes


def build_graph(node_inputs):
    graph = {}

    for node_input in node_inputs:
        nodes = parse_node_input(node_input)
        graph[nodes[0]] = [nodes[1], nodes[2]]

    return graph


def solve_part1(file):
    inputs = get_inputs(file)
    directions = inputs[0]
    graph = build_graph(inputs[2:])

    curr_node = "AAA"
    num_steps = 0
    dir_ind = 0

    while curr_node != "ZZZ":
        curr_dir = directions[dir_ind]
        curr_node = graph[curr_node][dir_map[curr_dir]]
        num_steps += 1
        dir_ind = (dir_ind + 1) % len(directions)

    print(num_steps)


def get_starting_nodes(graph):
    staring_nodes = [node for node in graph.keys() if node.endswith("A")]
    return staring_nodes


def check_all_nodes_ended(nodes):
    for node in nodes:
        if not node.endswith("Z"):
            return False

    return True


# Definitely did not yoink these functions
def gcd(a, b):
    if a == 0:
        return b
    return gcd(b % a, a)


def lcm(a, b):
    return (a // gcd(a, b)) * b


def solve_part2(file):
    inputs = get_inputs(file)
    directions = inputs[0]
    graph = build_graph(inputs[2:])

    nodes = get_starting_nodes(graph)
    num_steps_list = []

    ## This will take 10 years to run
    # while not check_all_nodes_ended(nodes):
    #     curr_dir = directions[dir_ind]
    #     for i, node in enumerate(nodes):
    #         nodes[i] = graph[node][dir_map[curr_dir]]
    #
    #     num_steps += 1
    #     dir_ind = (dir_ind + 1) % len(directions)
    #

    # LCM (Least Common Multiple) solution
    # We know that we want the the number of steps it takes for all nodes to end at a node that ends with Z
    # We also know that the graph are disconnected cycles, where each cycle is a node that ends with A
    # We just need to get the number of steps for each distinct cycle, and using LCM we can find the lowest number of steps where all the cycle syncs up

    for node in nodes:
        dir_ind = 0
        num_steps = 0
        while not node.endswith("Z"):
            curr_dir = directions[dir_ind]
            node = graph[node][dir_map[curr_dir]]
            num_steps += 1
            dir_ind = (dir_ind + 1) % len(directions)

        num_steps_list.append(num_steps)

    print(nodes)
    print(num_steps_list)
    lcm_steps = 1
    for num_steps in num_steps_list:
        lcm_steps = lcm(lcm_steps, num_steps)

    print(lcm_steps)


if __name__ == "__main__":
    import sys

    # solve_part1(sys.argv[1])
    solve_part2(sys.argv[1])
