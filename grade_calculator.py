"""Calculate a student's total, average, and pass/fail result for three subjects."""

from math import isfinite


def read_name():
    """Ask again if the student's name is empty."""
    while True:
        name = input("Student name: ").strip()
        if name:
            return name
        print("Please enter a non-empty student name.")


def read_score(subject_number):
    """Read one numeric score from 0 to 100, including decimal scores."""
    while True:
        try:
            score = float(input(f"Subject {subject_number} score (0-100): "))
        except ValueError:
            print("Please enter a number between 0 and 100.")
            continue

        if isfinite(score) and 0 <= score <= 100:
            return score
        print("Please enter a number between 0 and 100.")


def main():
    print("Student Grade Calculator")
    try:
        name = read_name()
        scores = [read_score(number) for number in range(1, 4)]
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled. No result calculated.")
        return 1

    total = sum(scores)
    average = total / 3
    result = "PASS" if average >= 60 else "FAIL"

    print("\nGrade Report")
    print(f"Student: {name}")
    for number, score in enumerate(scores, start=1):
        print(f"Subject {number}: {score:.2f}")
    print(f"Total: {total:.2f}")
    print(f"Average: {average:.2f}")
    print(f"Result: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
