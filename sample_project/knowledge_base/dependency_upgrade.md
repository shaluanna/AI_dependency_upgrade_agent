# Python Dependency Upgrade Runbook

## Before upgrading

1. Create a Git branch.
2. Record the currently installed versions.
3. Run the existing test suite.
4. Review dependency release notes.
5. Search the source code for deprecated APIs.

## During the upgrade

Upgrade dependencies in controlled steps.

Avoid upgrading every package simultaneously when compatibility
is uncertain.

## After upgrading

1. Install the new versions.
2. Run automated tests.
3. Review failures.
4. Check application startup.
5. Check integration points.
6. Review warnings and deprecated APIs.

## Rollback

If the application becomes unstable:

1. Restore the previous requirements file.
2. Reinstall previous versions.
3. Re-run tests.
4. Review the failed upgrade.