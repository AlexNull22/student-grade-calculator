"""Black-box checks for the single-file grade calculator.

Run from the project folder with:
    python -m unittest discover -s tests -v
"""

import math
import os
from pathlib import Path
import re
import subprocess
import sys
import unittest


PROGRAM = Path(__file__).resolve().parents[1] / "grade_calculator.py"
NUMBER = r"([-+]?\d+(?:\.\d+)?)"


class GradeCalculatorCLI(unittest.TestCase):
    def run_cli(self, user_input, allowed_returncodes=(0,)):
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [sys.executable, str(PROGRAM)],
            input=user_input,
            text=True,
            encoding="utf-8",
            capture_output=True,
            env=env,
            timeout=10,
        )
        self.assertIn(result.returncode, allowed_returncodes, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)
        self.assertEqual(result.stderr, "", result.stderr)
        return result.stdout

    def assert_summary(self, output, name, total, average, passed):
        self.assertIn(name, output)
        total_match = re.search(
            r"(?:Total(?:\s+Score)?|总分)\s*[:：=]\s*" + NUMBER,
            output,
            re.IGNORECASE,
        )
        average_match = re.search(
            r"(?:Average(?:\s+Score)?|平均(?:分)?)\s*[:：=]\s*" + NUMBER,
            output,
            re.IGNORECASE,
        )
        self.assertIsNotNone(total_match, output)
        self.assertIsNotNone(average_match, output)
        actual_total = float(total_match.group(1))
        actual_average = float(average_match.group(1))
        self.assertTrue(math.isfinite(actual_total))
        self.assertTrue(math.isfinite(actual_average))
        self.assertAlmostEqual(actual_total, total, delta=0.0051)
        self.assertAlmostEqual(actual_average, average, delta=0.0051)
        result_match = re.search(
            r"(?:Result|Status|结果|状态)\s*[:：=]\s*(PASS(?:ED)?|FAIL(?:ED)?|不及格|及格)",
            output,
            re.IGNORECASE,
        )
        self.assertIsNotNone(result_match, output)
        actual_status = result_match.group(1).lower()
        self.assertEqual(actual_status in ("pass", "passed", "及格"), passed, output)

    def test_normal_input(self):
        output = self.run_cli("Ada\n90\n80\n70\n")
        self.assert_summary(output, "Ada", 240, 80, True)

    def test_average_exactly_sixty_passes(self):
        output = self.run_cli("Boundary\n60\n60\n60\n")
        self.assert_summary(output, "Boundary", 180, 60, True)

    def test_average_below_sixty_fails(self):
        output = self.run_cli("Below\n60\n60\n59\n")
        self.assert_summary(output, "Below", 179, 179 / 3, False)

    def test_display_rounding_does_not_change_pass_fail(self):
        output = self.run_cli("Almost\n59.999\n59.999\n59.999\n")
        self.assert_summary(output, "Almost", 179.997, 59.999, False)

    def test_score_boundaries(self):
        for score, passed in ((0, False), (100, True)):
            with self.subTest(score=score):
                output = self.run_cli(f"Boundary {score}\n{score}\n{score}\n{score}\n")
                self.assert_summary(output, f"Boundary {score}", 3 * score, score, passed)

    def test_decimal_scores(self):
        output = self.run_cli("Decimals\n59.9\n60.1\n60\n")
        self.assert_summary(output, "Decimals", 180, 60, True)

    def test_invalid_input_retries(self):
        output = self.run_cli(
            "\n   \nRetry\nword\n-1\n101\nnan\nNaN\ninf\n-Infinity\n60\n60\n60\n"
        )
        self.assert_summary(output, "Retry", 180, 60, True)

    def test_unicode_name(self):
        output = self.run_cli("张小明 Zoë\n85\n90\n95\n")
        self.assert_summary(output, "张小明 Zoë", 270, 90, True)

    def test_end_of_input_exits_cleanly(self):
        for user_input in ("", "Partial\n", "Partial\n80\n"):
            with self.subTest(user_input=user_input):
                output = self.run_cli(user_input, allowed_returncodes=(0, 1))
                self.assertRegex(output, r"(?i)(?:cancel|exit|goodbye|end of input|结束|退出|取消)")
                self.assertNotRegex(output, r"(?:Result|Status|结果|状态)\s*[:：=]\s*(?:PASS|FAIL|及格|不及格)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
