import os
import sys


def create_input_files(path):
    input_path = os.path.join(path, "input.txt")
    example_input_path = os.path.join(path, "example_input.txt")

    with open(input_path, "w") as f:
        f.write("")

    with open(example_input_path, "w") as f:
        f.write("")


def create_python_file(path, new_day):
    python_file = os.path.join(path, f"{new_day}.py")

    with open(python_file, "w") as f:
        f.write(
            """\
def get_inputs(file):
    with open(file) as f:
        inputs = f.read().splitlines()

    return inputs


def solve_part1(file):
    inputs = get_inputs(file)
    print(inputs)


if __name__ == "__main__":
    import sys

    solve_part1(sys.argv[1])
    # solve_part2(sys.argv[1])
        """
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: 'python generate_new_day.py day<number>'")
        exit()

    new_day = sys.argv[1]
    cwd = os.getcwd()

    new_day_path = os.path.join(cwd, new_day)
    os.mkdir(new_day_path)

    create_input_files(new_day_path)
    create_python_file(new_day_path, new_day)

    print(f"{new_day} and associated files have been created in {new_day_path}")
