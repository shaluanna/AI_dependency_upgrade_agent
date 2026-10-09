from django.conf.urls import url


def health():
    return "OK"


def add(a, b):
    return a + b