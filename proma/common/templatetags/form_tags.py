from crispy_forms.utils import TEMPLATE_PACK
from django import template
from django.forms.boundfield import BoundField
from django.template import loader

register = template.Library()


@register.simple_tag(name='field')
def custom_field(field, **kwargs):
    """Use crispy_forms as a base template for custom form fields"""
    assert isinstance(field, BoundField), f'{field} must be an Field instance'
    template_path = '%s/field.html' % TEMPLATE_PACK
    context = {
        'field': field,
        'form_show_labels': kwargs.get('label', True),
        'form_show_errors': True,
    }

    template_ = loader.get_template(template_path)
    return template_.render(context)
