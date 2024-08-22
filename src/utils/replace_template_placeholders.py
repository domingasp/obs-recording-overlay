from typing import TypedDict


class TemplateReplacement(TypedDict):
    replace: str
    with_value: str


def replace_template_placeholders(
    template: str, replacements: list[TemplateReplacement]
):
    for replacement in replacements:
        template = template.replace(replacement["replace"], replacement["with_value"])

    return template
