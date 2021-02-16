from django.conf import settings

def pytest_configure():
    settings.configure(
        DEBUG=True,
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        ROOT_URLCONF='tests.test_django',
    )
