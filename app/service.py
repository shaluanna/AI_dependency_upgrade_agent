import json
import random
import time
from pathlib import Path

from dotenv import load_dotenv

from app.ai.gemini import generate_analysis
from app.ai.prompts import build_analysis_prompt
from app.ai.rag import retrieve_documents
from app.analyzers.ast_analyzer import analyze_project
from app.analyzers.pypi import check_dependencies
from app.analyzers.risk import calculate_risk
from app.analyzers.test_runner import run_tests
from app.core.dependency_parser import parse_requirements
from app.core.models import AnalysisReport


load_dotenv()


def generate_analysis_with_retry(
    prompt,
    report,
    max_retries=3
):
    for attempt in range(max_retries):
        try:
            result = generate_analysis(prompt)

            if result:
                result_text = str(result)

                temporary_error = (
                    "503" in result_text
                    or "UNAVAILABLE" in result_text
                    or "429" in result_text
                    or "RESOURCE_EXHAUSTED" in result_text
                    or "500" in result_text
                    or "504" in result_text
                )

                if not temporary_error:
                    return result

            if attempt < max_retries - 1:
                delay = (
                    (2 ** attempt)
                    + random.uniform(0, 1)
                )

                print(
                    f"\nGemini temporarily unavailable. "
                    f"Retrying in {delay:.1f} seconds..."
                )

                time.sleep(delay)

        except Exception as exc:
            error_text = str(exc)

            temporary_error = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
                or "500" in error_text
                or "504" in error_text
            )

            if not temporary_error:
                return (
                    "Gemini analysis could not be generated: "
                    f"{exc}"
                )

            if attempt < max_retries - 1:
                delay = (
                    (2 ** attempt)
                    + random.uniform(0, 1)
                )

                print(
                    f"\nGemini temporarily unavailable. "
                    f"Retrying in {delay:.1f} seconds..."
                )

                time.sleep(delay)

    return build_fallback_analysis(report)


def build_fallback_analysis(report):
    lines = [
        "Gemini AI analysis was temporarily unavailable.",
        "",
        "Fallback Compatibility Analysis",
        "--------------------------------",
        f"Risk level: {report.risk_level}",
        f"Risk score: {report.risk_score}",
        ""
    ]

    if report.dependencies:
        lines.append("Dependency Recommendations:")

        for dependency in report.dependencies:
            if dependency.update_available:
                lines.append(
                    f"- Review upgrade for "
                    f"{dependency.name}: "
                    f"{dependency.current_version} "
                    f"-> "
                    f"{dependency.latest_version}"
                )
            else:
                lines.append(
                    f"- {dependency.name}: "
                    f"no upgrade currently identified."
                )

        lines.append("")

    if report.code_findings:
        lines.append("Code Compatibility Findings:")

        for finding in report.code_findings:
            lines.append(
                f"- {finding.file}:"
                f"{finding.line} "
                f"{finding.issue}"
            )

            if finding.suggestion:
                lines.append(
                    f"  Recommendation: "
                    f"{finding.suggestion}"
                )

        lines.append("")

    else:
        lines.append(
            "No source-code compatibility findings "
            "were detected."
        )

        lines.append("")

    if report.test_result:
        lines.append("Test Status:")

        lines.append(
            f"- Passed: "
            f"{report.test_result.passed}"
        )

        lines.append(
            f"- Failed: "
            f"{report.test_result.failed}"
        )

        lines.append(
            f"- Skipped: "
            f"{report.test_result.skipped}"
        )

        lines.append(
            f"- Return code: "
            f"{report.test_result.return_code}"
        )

        lines.append("")

    lines.append("Recommended Next Steps:")

    lines.append(
        "- Review dependency upgrade compatibility."
    )

    lines.append(
        "- Review deprecated or legacy APIs "
        "identified by the source-code analyzer."
    )

    lines.append(
        "- Run the project test suite after "
        "applying compatibility changes."
    )

    return "\n".join(lines)


def analyze_project_dependencies(
    project_path: str,
    run_project_tests: bool = True
):
    project = Path(project_path)

    if not project.exists():
        raise FileNotFoundError(
            f"Project does not exist: {project}"
        )

    dependencies = parse_requirements(
        str(project)
    )

    package_results = check_dependencies(
        dependencies
    )

    code_findings = analyze_project(
        str(project)
    )

    report = AnalysisReport(
        project_path=str(project),
        dependencies=package_results,
        code_findings=code_findings
    )

    if run_project_tests:
        report.test_result = run_tests(
            str(project)
        )

    report = calculate_risk(report)

    knowledge_base = project / "knowledge_base"

    documentation = retrieve_documents(
        query=(
            "dependency upgrade compatibility "
            "migration deprecated API "
            "version upgrade"
        ),
        knowledge_base_path=knowledge_base,
        top_k=3
    )

    report.documentation = documentation

    prompt = build_analysis_prompt(
        report,
        documentation
    )

    report.ai_analysis = generate_analysis_with_retry(
        prompt,
        report
    )

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    output_file = (
        reports_dir /
        "upgrade_report.json"
    )

    output_file.write_text(
        json.dumps(
            report_to_dict(report),
            indent=4
        ),
        encoding="utf-8"
    )

    return report


def report_to_dict(report):
    return {
        "project_path": report.project_path,

        "dependencies": [
            {
                "name": item.name,
                "current_version": item.current_version,
                "latest_version": item.latest_version,
                "update_available": item.update_available,
                "error": item.error
            }
            for item in report.dependencies
        ],

        "code_findings": [
            {
                "file": item.file,
                "line": item.line,
                "issue": item.issue,
                "severity": item.severity,
                "suggestion": item.suggestion
            }
            for item in report.code_findings
        ],

        "test_result": (
            {
                "passed": report.test_result.passed,
                "failed": report.test_result.failed,
                "skipped": report.test_result.skipped,
                "return_code": report.test_result.return_code,
                "output": report.test_result.output
            }
            if report.test_result
            else None
        ),

        "risk_level": report.risk_level,
        "risk_score": report.risk_score,
        "documentation": report.documentation,
        "ai_analysis": report.ai_analysis
    }