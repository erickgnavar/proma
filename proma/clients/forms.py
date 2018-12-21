from django import forms

from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            "name",
            "email",
            "alias",
            "phone",
            "tax_identifier",
            "address",
            "state",
            "city",
            "country",
            "zipcode",
        )
