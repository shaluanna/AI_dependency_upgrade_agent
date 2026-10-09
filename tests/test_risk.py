from app.analyzers.risk import calculate_risk
from app.core.models import AnalysisReport, ASTFinding


def test_risk_calculation():
    report = AnalysisReport(
        project_path="sample_project",
        code_findings=[
            ASTFinding(
                file="app.py",
                line=1,
                issue="Deprecated API",
                severity="MEDIUM",
                suggestion="Use modern API"
            )
        ]
    )

    result = calculate_risk(report)

    assert result.risk_score == 2
    assert result.risk_level == "LOW"