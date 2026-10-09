import argparse

from app.analyzers.ast_analyzer import analyze_project
from app.analyzers.test_runner import run_tests
from app.core.dependency_parser import parse_requirements
from app.service import analyze_project_dependencies


def command_scan(project_path):
    dependencies = parse_requirements(project_path)

    print("\nDependencies:\n")

    for dependency in dependencies:
        print(
            f"{dependency.name} "
            f"{dependency.specifier or ''}"
        )


def command_test(project_path):
    result = run_tests(project_path)

    print("\nTest Results")
    print("------------")

    print(f"Passed : {result.passed}")
    print(f"Failed : {result.failed}")
    print(f"Skipped: {result.skipped}")
    print(f"Return : {result.return_code}")

    print("\nOutput:")
    print(result.output)


def command_analyze(project_path):
    report = analyze_project_dependencies(
        project_path,
        run_project_tests=True
    )

    print("\nAI Dependency Upgrade Analysis")
    print("--------------------------------")

    print(f"Risk level: {report.risk_level}")
    print(f"Risk score: {report.risk_score}")

    print("\nDependencies:")

    for dependency in report.dependencies:
        print(
            f"- {dependency.name}: "
            f"{dependency.current_version} -> "
            f"{dependency.latest_version}"
        )

    print("\nCode Findings:")

    for finding in report.code_findings:
        print(
            f"- {finding.file}:{finding.line} "
            f"{finding.issue}"
        )

    if report.ai_analysis:
        print("\nAI Analysis:")
        print(report.ai_analysis)


def main():
    parser = argparse.ArgumentParser(
        description="AI Dependency Upgrade and Compatibility Agent"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("project_path")

    test_parser = subparsers.add_parser("test")
    test_parser.add_argument("project_path")

    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("project_path")

    args = parser.parse_args()

    if args.command == "scan":
        command_scan(args.project_path)

    elif args.command == "test":
        command_test(args.project_path)

    elif args.command == "analyze":
        command_analyze(args.project_path)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()