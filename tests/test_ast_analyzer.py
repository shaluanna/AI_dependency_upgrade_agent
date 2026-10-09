from pathlib import Path

from app.analyzers.ast_analyzer import analyze_python_file


def test_detect_legacy_django_url(tmp_path: Path):
    source_file = tmp_path / "example.py"

    source_file.write_text(
        "from django.conf.urls import url\n",
        encoding="utf-8"
    )

    findings = analyze_python_file(source_file)

    assert len(findings) == 1
    assert findings[0].severity == "MEDIUM"