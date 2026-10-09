import subprocess


def is_git_repository(project_path: str):
    result = subprocess.run(
        [
            "git",
            "-C",
            project_path,
            "rev-parse",
            "--is-inside-work-tree"
        ],
        capture_output=True,
        text=True
    )

    return (
        result.returncode == 0
        and result.stdout.strip() == "true"
    )


def create_upgrade_branch(
    project_path: str,
    branch_name="ai/dependency-upgrade"
):
    if not is_git_repository(project_path):
        return {
            "success": False,
            "message": "Not a Git repository."
        }

    result = subprocess.run(
        [
            "git",
            "-C",
            project_path,
            "checkout",
            "-b",
            branch_name
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {
            "success": False,
            "message": result.stderr.strip()
        }

    return {
        "success": True,
        "message": f"Created branch: {branch_name}"
    }