import re
import subprocess
import sys

from app.core.models import TestResult


def run_tests(project_path: str) -> TestResult:
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q"
    ]

    try:
        process = subprocess.run(
            command,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=120
        )

        output = (
            process.stdout +
            "\n" +
            process.stderr
        )

        passed = 0
        failed = 0
        skipped = 0

        passed_match = re.search(
            r"(\d+)\s+passed",
            output
        )

        failed_match = re.search(
            r"(\d+)\s+failed",
            output
        )

        skipped_match = re.search(
            r"(\d+)\s+skipped",
            output
        )

        if passed_match:
            passed = int(
                passed_match.group(1)
            )

        if failed_match:
            failed = int(
                failed_match.group(1)
            )

        if skipped_match:
            skipped = int(
                skipped_match.group(1)
            )

        return TestResult(
            passed=passed,
            failed=failed,
            skipped=skipped,
            return_code=process.returncode,
            output=output
        )

    except subprocess.TimeoutExpired:
        return TestResult(
            return_code=-1,
            output="Test execution timed out."
        )

    except Exception as exc:
        return TestResult(
            return_code=-1,
            output=str(exc)
        )