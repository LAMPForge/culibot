import datetime
from typing import Mapping, Any

from jinja2 import (
    ChoiceLoader,
    Environment,
    PackageLoader,
    PrefixLoader,
    StrictUndefined,
    select_autoescape,
)

EMAIL_TEMPLATES_FOLDER_NAME = "email_templates"


class EmailRenderer:
    def __init__(self, extras_templates_packages: Mapping[str, str] = {}) -> None:
        self.env = Environment(
            loader=ChoiceLoader(
                [
                    PackageLoader("culi.email", EMAIL_TEMPLATES_FOLDER_NAME),
                    PrefixLoader(
                        {
                            prefix: PackageLoader(package, EMAIL_TEMPLATES_FOLDER_NAME)
                            for prefix, package in extras_templates_packages.items()
                        }
                    ),
                ]
            ),
            autoescape=select_autoescape(),
            undefined=StrictUndefined,
        )

    def render_from_string(
        self, subject: str, body: str, context: dict[str, Any]
    ) -> tuple[str, str]:
        rendered_subject = self.env.from_string(subject).render(context).strip()

        wrapped_body = f"""
        {{% extends 'base.html' %}}

        {{% block body %}}
            {body}
        {{% endblock %}}
        """

        context["current_year"] = datetime.datetime.now().year

        rendered_body = self.env.from_string(wrapped_body).render(context).strip()
        return rendered_subject, rendered_body

    def render_from_template(
        self, subject: str, body_template: str, context: dict[str, Any]
    ) -> tuple[str, str]:
        rendered_subject = self.env.from_string(subject).render(context).strip()
        rendered_body = self.env.get_template(body_template).render(context).strip()
        return rendered_subject, rendered_body


def get_email_renderer(
    extras_templates_packages: Mapping[str, str] = {},
) -> EmailRenderer:
    return EmailRenderer(extras_templates_packages)
