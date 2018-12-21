from crispy_forms.helper import FormHelper


class CommonFilterHelper(FormHelper):

    form_tag = False
    disable_csrf = True
    field_template = "bootstrap4/layout/inline_field.html"
