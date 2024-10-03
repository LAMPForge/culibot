from enum import Enum, auto
from typing import TypeVar, Generic, TypeGuard

from culi.auth.scope import Scope
from culi.models.user import User


class Anonymous: ...


Subject = User | Anonymous
SubjectType = type[User] | type[Anonymous]
SUBJECTS: set[SubjectType] = {User, Anonymous}


class AuthMethod(Enum):
    NONE = auto()
    COOKIE = auto()


S = TypeVar("S", bound=Subject, covariant=True)


class AuthSubject(Generic[S]):
    subject: S
    scopes: set[Scope]
    method: AuthMethod

    def __init__(self, subject: S, scopes: set[Scope], method: AuthMethod) -> None:
        self.subject = subject
        self.scopes = scopes
        self.method = method

    def has_web_default_scope(self) -> bool:
        return Scope.web_default in self.scopes


def is_anonymous(auth_subject: AuthSubject[S]) -> TypeGuard[AuthSubject[Anonymous]]:
    return isinstance(auth_subject.subject, Anonymous)


def is_user(auth_subject: AuthSubject[S]) -> TypeGuard[AuthSubject[User]]:
    return isinstance(auth_subject.subject, User)


__all__ = [
    "Anonymous",
    "Subject",
    "SubjectType",
    "SUBJECTS",
    "AuthMethod",
    "AuthSubject",
    "is_anonymous",
    "is_user",
]