
def parse_input(path: str) -> list[list[int]]:
    result = []
    with open(path) as file:
        for line in file.readlines():
            result.append([int(i) for i in line.split()])
    return result


def is_valid_report(report: list[int]) -> bool:
    if report[0] < report[1]:
        asc = True
    else:
        asc = False
    prev = report[1]
    if not (1 <= abs(prev - report[0]) <= 3):
        return False
    for i in range(2, len(report)):
        if asc and prev >= report[i] or not asc and prev <= report[i] or not (1 <= abs(prev - report[i]) <= 3):
            return False
        prev = report[i]
    return True

def count_valid_reports(reports: list[list[int]]) -> int:
    result = 0
    for report in reports:
        if is_valid_report(report):
            result += 1
    return result


def count_valid_reports_with_problem_dampener(reports: list[list[int]]) -> int:
    result = 0
    for report in reports:
        if is_valid_report(report):
            result += 1
        else:
            for i in range(len(report)):  # not the fastest to run but the fastest to code :)
                without_i = report[:i] + report[i + 1:]
                if is_valid_report(without_i):
                    result += 1
                    break
    return result



def main():
    print("Example result:", count_valid_reports(parse_input("example-input.txt")))
    print("Task result:", count_valid_reports(parse_input("input.txt")))
    print("--- 2 ---")
    print("Example result:", count_valid_reports_with_problem_dampener(parse_input("example-input.txt")))
    print("Task result:", count_valid_reports_with_problem_dampener(parse_input("input.txt")))


if __name__ == '__main__':
    main()