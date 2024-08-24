from django import template
register = template.Library()

@register.filter(name='add_input_validation')
def add_input_validation(field):
    if field.field.widget.input_type == 'text':
        field.field.widget.attrs.update({
            'maxlength': '150',
            'required': 'required',
            'pattern': '[A-Za-z0-9]+',
            'title': 'Username should only contain letters and numbers.',
            'autocomplete': 'off'
        })
    elif field.field.widget.input_type == 'password':
        field.field.widget.attrs.update({
            'required': 'required',
            'minlength': '8',
            'title': 'Password must be at least 8 characters long.',
            'autocomplete': 'off'
        })
    return field
