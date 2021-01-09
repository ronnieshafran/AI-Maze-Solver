from numpy import random


def generate_random_matrix(size):
    return random.uniform(0, 100, (size, size))


def get_rows_and_cols(size):
    return random.randint(0, size - 1), random.randint(0, size - 1)


def insert_blocks(matrix, size):
    number_of_blocks = random.randint(1, (size ** 2) / 2)
    while number_of_blocks != 0:
        rows, cols = get_rows_and_cols(size)
        if matrix[rows][cols] == -1:
            continue
        matrix[rows][cols] = -1
        number_of_blocks -= 1


def parse_matrix(matrix):
    for row in matrix:
        for col in row:
            if col != row[-1]:
                print(round(col, 2), ',', end="")
            else:
                print(round(col, 2), end="")
        print()


def get_point(matrix, size):
    value = -1
    rows = -1
    cols = -1
    while value == -1:
        rows, cols = get_rows_and_cols(size)
        value = matrix[rows][cols]
    return rows, cols


if __name__ == '__main__':
    algorithms = ["UCS", "IDS", "ASTAR", "BIASTAR", "IDA"]
    size = random.randint(5, 15)
    matrix = generate_random_matrix(size)
    insert_blocks(matrix, size)
    print(random.choice(algorithms))
    print(size)
    print(f'{get_point(matrix, size)[0]},{get_point(matrix, size)[1]}')
    print(f'{get_point(matrix, size)[0]},{get_point(matrix, size)[1]}')
    parse_matrix(matrix)
