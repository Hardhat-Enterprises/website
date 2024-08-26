from django import template

register = template.Library()


@register.filter(name="add_input_validation")
def add_input_validation(field):
    if field.field.widget.input_type == "text":
        field.field.widget.attrs.update(
            {
                "required": "required",
                "pattern": "[a-zA-Z0-9]+@deakin.edu.au",
                "title": "Please enter a valid company email address (e.g., example@deakin.edu.au).",
                "autocomplete": "off",
            }
        )
    elif field.field.widget.input_type == "password":
        field.field.widget.attrs.update(
            {
                "required": "required",
                "minlength": "8",
                "title": "Password must be at least 8 characters long.",
                "autocomplete": "off",
            }
        )
    return field
