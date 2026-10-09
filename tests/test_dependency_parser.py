from pathlib import Path

from app.core.dependency_parser import parse_requirements


def test_parse_requirements(tmp_path: Path):
    requirements = tmp_path / "requirements.txt"

    requirements.write_text(
        """
Django==4.2.10
requests>=2.31.0
numpy
""",
        encoding="utf-8"
    )

    dependencies = parse_requirements(
        str(tmp_path)
    )

    assert len(dependencies) == 3

    assert dependencies[0].name == "Django"
    assert dependencies[0].current_version == "4.2.10"

    assert dependencies[1].name == "requests"
    assert dependencies[1].specifier == ">=2.31.0"

    assert dependencies[2].name == "numpy"