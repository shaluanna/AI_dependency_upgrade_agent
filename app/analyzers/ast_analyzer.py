import ast
from pathlib import Path

from app.core.models import ASTFinding


DEPRECATED_PATTERNS = {
    ("django.urls", "url"): {
        "issue": "Potentially deprecated Django URL API",
        "severity": "MEDIUM",
        "suggestion": "Consider using path() or re_path()."
    },
    ("django.conf.urls", "url"): {
        "issue": "Legacy Django URL import",
        "severity": "MEDIUM",
        "suggestion": "Consider migrating to django.urls.path() or re_path()."
    }
}


SKIP_DIRECTORIES = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    "node_modules"
}


def analyze_python_file(file_path: Path):
    findings = []

    try:
        source = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        tree = ast.parse(
            source,
            filename=str(file_path)
        )

    except Exception:
        return findings

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):

            module = node.module

            if not module:
                continue

            for imported_name in node.names:
                key = (
                    module,
                    imported_name.name
                )

                if key not in DEPRECATED_PATTERNS:
                    continue

                info = DEPRECATED_PATTERNS[key]

                findings.append(
                    ASTFinding(
                        file=str(file_path),
                        line=node.lineno,
                        issue=info["issue"],
                        severity=info["severity"],
                        suggestion=info["suggestion"]
                    )
                )

    return findings


def analyze_project(project_path: str):
    project = Path(project_path)
    findings = []

    for file_path in project.rglob("*.py"):

        if any(
            part in SKIP_DIRECTORIES
            for part in file_path.parts
        ):
            continue

        findings.extend(
            analyze_python_file(file_path)
        )

    return findings