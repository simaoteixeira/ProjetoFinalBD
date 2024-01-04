from django import forms

class WarehousesForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, error_messages={'required': 'Campo obrigatório', 'max_length': 'Nome muito longo'})
    location = forms.CharField(max_length=100, required=True, error_messages={'required': 'Campo obrigatório', 'max_length': 'Localização muito longa'})

    class Meta:
        fields = ['name', 'location']