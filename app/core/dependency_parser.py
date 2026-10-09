import re
from pathlib import Path
from typing import List

from app.core.models import Dependency


REQUIREMENT_PATTERN = re.compile(
    r"^\s*([A-Za-z0-9_.-]+)\s*"
    r"(?:([<>=!~]{1,3})\s*([A-Za-z0-9.*+!\-]+))?"
)


def parse_requirements(project_path: str) -> List[Dependency]:
    project = Path(project_path)

    requirement_file = None

    for filename in [
        "requirements.txt",
        "requirements.in"
    ]:
        candidate = project / filename

        if candidate.exists():
            requirement_file = candidate
            break

    if requirement_file is None:
        return []

    dependencies = []

    lines = requirement_file.read_text(
        encoding="utf-8",
        errors="ignore"
    ).splitlines()

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        if line.startswith("-"):
            continue

        match = REQUIREMENT_PATTERN.match(line)

        if not match:
            continue

        name = match.group(1)
        operator = match.group(2)
        version = match.group(3)

        specifier = None

        if operator and version:
            specifier = f"{operator}{version}"

        dependencies.append(
            Dependency(
                name=name,
                current_version=version,
                specifier=specifier
            )
        )

    return dependencies