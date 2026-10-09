def build_analysis_prompt(report, documentation):
    dependencies = []

    for item in report.dependencies:
        dependencies.append(
            f"- {item.name}: "
            f"{item.current_version} -> "
            f"{item.latest_version}"
        )

    findings = []

    for item in report.code_findings:
        findings.append(
            f"- {item.file}:{item.line} | "
            f"{item.severity} | "
            f"{item.issue} | "
            f"{item.suggestion}"
        )

    docs = "\n\n".join(documentation)

    if report.test_result:
        test_results = (
            f"Passed: {report.test_result.passed}\n"
            f"Failed: {report.test_result.failed}\n"
            f"Skipped: {report.test_result.skipped}\n"
            f"Return code: {report.test_result.return_code}\n\n"
            f"Output:\n{report.test_result.output}"
        )
    else:
        test_results = "Tests were not executed."

    prompt = f"""
You are a senior Python dependency migration engineer.

Review the project information below and provide a practical
compatibility assessment.

Project:
{report.project_path}

Risk level:
{report.risk_level}

Risk score:
{report.risk_score}

Dependencies:
{chr(10).join(dependencies)}

Code findings:
{chr(10).join(findings)}

Test results:
{test_results}

Relevant documentation:
{docs}

Provide the response under these headings:

1. Overall risk
2. Important compatibility issues
3. Dependencies that need attention
4. Required or likely code changes
5. Recommended upgrade order
6. Testing and validation plan
7. Rollback considerations

Use only the information provided above.
Do not invent package versions or project details.
Separate confirmed findings from recommendations.
Do not describe an upgrade as safe unless the available evidence supports it.
"""

    return prompt