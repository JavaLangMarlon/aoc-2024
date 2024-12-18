import numpy as np


def parse_input(filename: str) -> (np.ndarray, np.ndarray):
    list1 = []
    list2 = []
    sep = "   "
    with open(filename) as file:
        for line in file.readlines():
            args = line.strip().split(sep)
            list1.append(int(args[0]))
            list2.append(int(args[1]))
    return np.array(list1), np.array(list2)


def calculate_distance(list1: np.ndarray, list2: np.ndarray) -> float:
    list1.sort()
    list2.sort()
    return np.sum(np.abs(list1 - list2))

def calculate_similarity_score(list1: np.ndarray, list2: np.ndarray) -> float:
    score = 0
    for i in list1:
        score += i * np.sum(list2 == i)
    return score

def main():
    list1 = np.array([
        3, 4, 2, 1, 3, 3
    ])
    list2 = np.array([
        4, 3, 5, 3, 9, 3
    ])
    real_list1, real_list2 = parse_input("input.txt")
    print("Task 1 test result:", calculate_distance(list1, list2))
    print("Task 1 result:", calculate_distance(real_list1, real_list2))
    print("Task 2 test result:", calculate_similarity_score(list1, list2))
    print("Task 2 result:", calculate_similarity_score(real_list1, real_list2))

if __name__ == '__main__':
    main()
