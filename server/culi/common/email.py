import functools

import email_validator
from email_validator import EmailNotValidError, caching_resolver
from email_validator import validate_email as _validate_email


_email_dns_resolver = caching_resolver()

validate_email = functools.partial(
    _validate_email, check_deliverability=True, dns_resolver=_email_dns_resolver
)

__all__ = ["EmailNotValidError", "validate_email"]
