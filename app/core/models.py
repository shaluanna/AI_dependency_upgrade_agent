from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Dependency:
    name: str
    current_version: Optional[str] = None
    specifier: Optional[str] = None


@dataclass
class PackageInfo:
    name: str
    current_version: Optional[str]
    latest_version: Optional[str]
    update_available: bool
    error: Optional[str] = None


@dataclass
class ASTFinding:
    file: str
    line: int
    issue: str
    severity: str
    suggestion: str


@dataclass
class TestResult:
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    return_code: int = 0
    output: str = ""


@dataclass
class AnalysisReport:
    project_path: str
    dependencies: List[PackageInfo] = field(
        default_factory=list
    )
    code_findings: List[ASTFinding] = field(
        default_factory=list
    )
    test_result: Optional[TestResult] = None
    risk_level: str = "LOW"
    risk_score: int = 0
    documentation: List[str] = field(
        default_factory=list
    )
    ai_analysis: Optional[str] = None