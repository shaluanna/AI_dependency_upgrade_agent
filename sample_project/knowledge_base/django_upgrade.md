# Django Upgrade Notes

## URL routing

Older Django applications may contain legacy URL APIs such as:

```python
django.conf.urls.url
```

or:

```python
django.urls.url
```

For newer Django projects, these are generally replaced with:

```python
django.urls.path
```

and:

```python
django.urls.re_path
```

## Upgrade process

Before upgrading Django:

1. Check the version currently used by the project.
2. Check which Python versions are supported by the target Django version.
3. Review the relevant Django release notes.
4. Search the source code for deprecated APIs.
5. Run the existing test suite.

After the upgrade:

1. Run the test suite again.
2. Start the development server.
3. Check URL routing.
4. Check models and migrations.
5. Check templates.
6. Check authentication.
7. Review Django warnings and deprecation messages.
