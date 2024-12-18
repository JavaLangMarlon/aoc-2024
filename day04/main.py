from typing import Callable

horizontally_forward = lambda i, j: (i, j + 1)
horizontally_backward = lambda i, j: (i, j - 1)
vertically_forward = lambda i, j: (i + 1, j)
vertically_backward = lambda i, j: (i - 1, j)
diagonally_forward_downwards = lambda i, j: (i + 1, j + 1)
diagonally_forward_upwards = lambda i, j: (i - 1, j + 1)
diagonally_backward_downwards = lambda i, j: (i + 1, j - 1)
diagonally_backward_upwards = lambda i, j: (i - 1, j - 1)

potential_steps = [
    horizontally_forward, horizontally_backward, vertically_forward,
    vertically_backward, diagonally_forward_downwards, diagonally_forward_upwards,
    diagonally_backward_downwards, diagonally_backward_upwards,
]

def parse_input(path: str) -> list[str]:
    with open(path) as f:
        # assuming that all rows have the same length
        return f.read().split("\n")


def is_word_occurrence(text_matrix: list[str], word: str, i: int, j: int,
                       step: Callable[[int, int], tuple[int, int]]) -> bool:
    checked_letters = 0
    while checked_letters < len(word):
        if i > len(text_matrix) - 1 or j > len(text_matrix[0]) - 1 or i < 0 or j < 0:
            return False
        if text_matrix[i][j] != word[checked_letters]:
            return False
        checked_letters += 1

        i, j = step(i, j)
    return True


def count_words(text_matrix: list[str], word: str) -> int:
    # note: there are probably variants of this algorithm which are a lot faster
    result = 0
    for i in range(len(text_matrix)):
        for j in range(len(text_matrix[0])):  # we're doing hard assumptions here, see above
            if text_matrix[i][j] != word[0]:
                continue
            for step in potential_steps:
                if is_word_occurrence(text_matrix, word, i, j, step):
                    result += 1
    return result

def count_word_crosses(text_matrix: list[str]) -> int:
    result = 0
    # idkkkk
    for i in range(len(text_matrix) - 2):
        for j in range(len(text_matrix[0]) - 2):
            if text_matrix[i+1][j+1] == 'A' and (
                text_matrix[i][j] == 'M' and (
                    text_matrix[i][j+2] == 'M' and text_matrix[i+2][j] == 'S' and text_matrix[i+2][j+2] == 'S'
                    or
                    text_matrix[i][j + 2] == 'S' and text_matrix[i + 2][j] == 'M' and text_matrix[i + 2][j + 2] == 'S'
                ) or text_matrix[i][j] == 'S' and (
                    text_matrix[i][j + 2] == 'S' and text_matrix[i + 2][j] == 'M' and text_matrix[i + 2][j + 2] == 'M'
                    or
                    text_matrix[i][j + 2] == 'M' and text_matrix[i + 2][j] == 'S' and text_matrix[i + 2][j + 2] == 'M'
                )
            ):  # I love my life
                result += 1
    # this boolean expression can probably be optimized but my work shift starts now
    return result


def main():
    word = "XMAS"
    print("=== 1 ===")
    print("Example result:", count_words(parse_input("example-input.txt"), word))
    print("Puzzle result:", count_words(parse_input("input.txt"), word))
    print("=== 2 ===")
    print("Example result:", count_word_crosses(parse_input("example-input.txt")))
    print("Puzzle result:", count_word_crosses(parse_input("input.txt")))


if __name__ == "__main__":
    main()
