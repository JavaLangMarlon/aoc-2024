import re


expr_regex = re.compile(r'mul\([0-9]{1,3},[0-9]{1,3}\)')
expr_regex_with_do = re.compile(r'mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don\'t\(\)')
expr_prefix = "mul("
expr_suffix = ")"
expr_delimiter = ","
do = "do()"
dont = "don't()"


def parse_input(path: str) -> str:
    with open(path) as f:
        return f.read()


def add_mults(expression: str) -> int:
    result = 0
    for mult in expr_regex.findall(expression):
        nums = mult.replace(expr_prefix, "").replace(expr_suffix, "").split(expr_delimiter)
        result += int(nums[0]) * int(nums[1])
    return result


def add_mults_with_do(expression: str) -> int:
    enabled = True
    result = 0
    for hit in expr_regex_with_do.findall(expression):
        if hit == do:
            enabled = True
        elif hit == dont:
            enabled = False
        elif enabled:
            nums = hit.replace(expr_prefix, "").replace(expr_suffix, "").split(expr_delimiter)
            result += int(nums[0]) * int(nums[1])
    return result

def main():
    print("--- 1 ---")
    print("Example result:", add_mults(parse_input("example-input.txt")))
    print("Exercise result:", add_mults(parse_input("input.txt")))
    print("--- 2 ---")
    print("Example result:", add_mults_with_do(parse_input("example2-input.txt")))
    print("Exercise result:", add_mults_with_do(parse_input("input.txt")))



if __name__ == '__main__':
    main()
