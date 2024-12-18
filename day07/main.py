import itertools

operators = (
    lambda x, y: x + y,
    lambda x, y: x * y,
)

# not very efficient, I know
operators_with_concatenation = operators + (
    lambda x, y: int(str(x) + str(y)),
)

def parse_input(path: str) -> list[tuple[int, list[int]]]:
    result = []
    sep = ": "
    with open(path) as file:
        for line in file:
            args = line.strip().split(sep)
            result.append((int(args[0]), [int(num) for num in args[1].split()]))
    return result

def calculate_calibration(equations: list[tuple[int, list[int]]],
                          used_operators=operators) -> int:
    """
    for simplicity, this time we will just use an exponential bruteforce algorithm
    """
    result = 0
    for equation in equations:
        for operator_series in itertools.product(used_operators, repeat=len(equation[1]) - 1):
            calibration = equation[1][0]
            for element_index in range(1, len(equation[1])):
                calibration = operator_series[element_index - 1](calibration, equation[1][element_index])
            if calibration == equation[0]:
                result += calibration
                break
    return result


def main():
    print("=== 1 ===")
    print("Example result:", calculate_calibration(parse_input("example-input.txt")))
    print("Task result:", calculate_calibration(parse_input("input.txt")))
    print("=== 2 ===")
    print("Example result:", calculate_calibration(parse_input("example-input.txt"), operators_with_concatenation))
    print("Task result:", calculate_calibration(parse_input("input.txt"), operators_with_concatenation))

if __name__ == "__main__":
    main()
