from app.core.models import AnalysisReport


def calculate_risk(report: AnalysisReport):
    score = 0

    for finding in report.code_findings:
        severity = finding.severity.upper()

        if severity == "HIGH":
            score += 3
        elif severity == "MEDIUM":
            score += 2
        elif severity == "LOW":
            score += 1

    for dependency in report.dependencies:
        if dependency.error:
            score += 2
        elif dependency.update_available:
            score += 1

    if report.test_result:

        if report.test_result.failed > 0:
            score += 4

        if report.test_result.return_code != 0:
            score += 2

    if score >= 8:
        level = "HIGH"
    elif score >= 4:
        level = "MEDIUM"
    else:
        level = "LOW"

    report.risk_score = score
    report.risk_level = level

    return report