# Sample Project Upgrade Notes

## Django

Older Django projects may still use the legacy URL APIs:

* `django.conf.urls.url`
* `django.urls.url`

When updating the project, check the URL configuration and consider replacing these with the newer APIs:

* `django.urls.path`
* `django.urls.re_path`

After making the changes, run the existing test suite to make sure the application still works as expected.

## Requests

When upgrading the `requests` package, check the areas that are most likely to be affected:

* Authentication behaviour
* Timeout handling
* Response handling
* Deprecated APIs
* Existing test coverage
