from inspect import Parameter, Signature
from typing import Annotated

from fastapi import Depends, Request, Security
from makefun import with_signature

from culi.auth.scope import RESERVED_SCOPES, Scope
from culi.config import settings
from culi.exceptions import NotPermitted, Unauthorized
from culi.postgres import AsyncSession, get_db_session
from .models import AuthMethod, AuthSubject, Anonymous, SubjectType, SUBJECTS, Subject, is_anonymous

from .service import AuthService
from ..models.user import User


async def _get_cookie_token(request: Request) -> str | None:
    return request.cookies.get(settings.AUTH_COOKIE_KEY)


async def get_auth_subject(
    cookie_token: str | None = Depends(_get_cookie_token),
    session: AsyncSession = Depends(get_db_session),
) -> AuthSubject[Subject]:
    if cookie_token is not None:
        user = await AuthService.get_user_from_cookie(session, cookie=cookie_token)
        if user:
            scopes = {Scope.web_default}
            return AuthSubject(user, scopes, AuthMethod.COOKIE)
    return AuthSubject(Anonymous(), set(), AuthMethod.NONE)


class _Authenticator:
    def __init__(
        self,
        *,
        allowed_subjects: set[SubjectType] = SUBJECTS,
        required_scopes: set[Scope] | None = None,
    ) -> None:
        self.allowed_subjects = allowed_subjects
        self.required_scopes = required_scopes

    async def __call__(
        self, auth_subject: AuthSubject[Subject]
    ) -> AuthSubject[Subject]:
        if is_anonymous(auth_subject):
            if Anonymous in self.allowed_subjects:
                return auth_subject
            else:
                raise Unauthorized()

        # Not allowed subject
        subject_type = type(auth_subject.subject)
        if subject_type not in self.allowed_subjects:
            raise InvalidTokenError(
                "The subject of this access token is not valid for this endpoint.",
                allowed_subjects=" ".join(s.__name__ for s in self.allowed_subjects),
            )

        # No required scopes
        if not self.required_scopes:
            return auth_subject

        # Have at least one of the required scopes. Allow this request.
        if auth_subject.scopes & self.required_scopes:
            return auth_subject

        raise InsufficientScopeError({s for s in self.required_scopes})


def Authenticator(
    allowed_subjects: set[SubjectType] = SUBJECTS,
    required_scopes: set[Scope] | None = None,
) -> _Authenticator:
    parameters: list[Parameter] = [
        Parameter(name="self", kind=Parameter.POSITIONAL_OR_KEYWORD),
        Parameter(
            name="auth_subject",
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            default=Security(
                get_auth_subject,
                scopes=sorted([
                    s.value
                    for s in (required_scopes or {})
                    if s not in RESERVED_SCOPES
                ]),
            ),
        ),
    ]
    signature = Signature(parameters)

    class _AuthenticatorSignature(_Authenticator):
        @with_signature(signature)
        async def __call__(
            self, auth_subject: AuthSubject[Subject]
        ) -> AuthSubject[Subject]:
            return await super().__call__(auth_subject)

    return _AuthenticatorSignature(
        allowed_subjects=allowed_subjects, required_scopes=required_scopes
    )


_WebUserOrAnonymous = Authenticator(
    allowed_subjects={Anonymous, User}, required_scopes={Scope.web_default}
)
WebUserOrAnonymous = Annotated[
    AuthSubject[Anonymous | User], Depends(_WebUserOrAnonymous)
]

_WebUser = Authenticator(allowed_subjects={User}, required_scopes={Scope.web_default})
WebUser = Annotated[AuthSubject[User], Depends(_WebUser)]

_AdminUser = Authenticator(allowed_subjects={User}, required_scopes={Scope.admin})
AdminUser = Annotated[AuthSubject[User], Depends(_AdminUser)]
