
def parse_input(path: str) -> tuple[dict[str, list[str]], list[list[str]]]:
    rules = {}
    updates = []
    with open(path) as f:
        reached_updates = False
        for line in f.readlines():
            stripped_line = line.strip()
            if reached_updates:
                updates.append(stripped_line.split(','))
            elif len(stripped_line.strip()) == 0:
                reached_updates = True
            else:
                vals = stripped_line.split('|')
                if vals[0] not in rules.keys():
                    rules[vals[0]] = [vals[1]]
                else:
                    rules[vals[0]].append(vals[1])
    return rules, updates


def is_valid_update(update: list[str], rules: dict[str, list[str]]) -> bool:
    seen_values = set()
    for i in update:
        seen_values.add(i)
        if i not in rules.keys():
            continue
        for successor in rules[i]:
            if successor in seen_values:
                return False
    return True


def count_value(rules: dict[str, list[str]], updates: list[list[str]]) -> int:
    result = 0
    for update in updates:
        if is_valid_update(update, rules):
            result += int(update[int(len(update) / 2)])
    return result


def dfs_visit(result: list[str], update: list[str], number: str,
              visited_numbers: set, rules: dict[str, list[str]]):
    visited_numbers.add(number)
    if number in rules.keys():
        for successor in rules[number]:
            if successor not in visited_numbers and successor in update:
                dfs_visit(result, update, successor, visited_numbers, rules)
    result.insert(0, number)


def sort_update(update: list[str], rules: dict[str, list[str]]) -> list[str]:
    # we can perform topological sorting here
    result = []
    visited_numbers = set()
    for i in update:
        if i not in visited_numbers:
            dfs_visit(result, update, i, visited_numbers, rules)
    return result



def count_value_of_unordered(rules: dict[str, list[str]], updates: list[list[str]]) -> int:
    result = 0
    for update in updates:
        if not is_valid_update(update, rules):
            result += int(sort_update(update, rules)[int(len(update) / 2)])
    return result


def main():
    print("==== 1 ====")
    print("Example result:", count_value(*parse_input("example-input.txt")))
    print("Task result:", count_value(*parse_input("input.txt")))
    print("==== 2 ====")
    print("Example result:", count_value_of_unordered(*parse_input("example-input.txt")))
    print("Task result:", count_value_of_unordered(*parse_input("input.txt")))


if __name__ == '__main__':
    main()