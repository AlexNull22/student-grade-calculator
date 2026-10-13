# Student Grade Calculator

A small, interactive Python script for one student and three subjects.

## Run

Requires Python 3.6 or newer. No third-party packages, accounts, or internet connection are needed.

```text
python grade_calculator.py
```

On Windows, `py grade_calculator.py` also works if the Python launcher is installed.

Enter the student's name, followed by the score for each of the three subjects. The program prints the total, average, and PASS or FAIL. An average of **60 or greater passes**.

## Example

```text
Student Grade Calculator
Student name: Alex
Subject 1 score (0-100): 80
Subject 2 score (0-100): 70
Subject 3 score (0-100): 90

Grade Report
Student: Alex
Subject 1: 80.00
Subject 2: 70.00
Subject 3: 90.00
Total: 240.00
Average: 80.00
Result: PASS
```

## Input rules

- Student names cannot be empty. Unicode names are supported in a compatible terminal.
- Scores are assumed to use a 0–100 scale. Whole numbers and decimal scores are accepted.
- Invalid scores prompt for another attempt. Negative numbers, numbers above 100, NaN, and infinity are rejected.
- Results are displayed to two decimal places. Pass/fail uses the calculated average before display rounding.
- Ctrl+C or end-of-input exits without calculating a partial report, with exit code 1.

## Tests

The acceptance tests use Python 3.7 or newer and only the standard library. Run from the repository root:

```text
python -m unittest discover -s tests -v
```

Nine test methods cover normal scores, the pass/fail boundary, decimals, display rounding, invalid inputs, Unicode names, and end-of-input cancellation.

## Files

- `grade_calculator.py`: the complete deliverable requested in the job post.
- `README.md`: optional usage instructions.
- `tests/test_grade_calculator.py`: independent command-line acceptance tests.
- `evidence/qa_results.txt`: recorded test output and independent review.
- `evidence/sample_run.txt`: output from a sample execution.
