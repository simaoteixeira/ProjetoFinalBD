from django import forms

class LaborsForm(forms.Form):
    title = forms.CharField(max_length=100, required=True, error_messages={'required': 'Campo obrigatório', 'max_length': 'Designação muito longa'})
    cost = forms.DecimalField(max_digits=5, decimal_places=2, required=True, error_messages={'required': 'Campo obrigatório', 'invalid': 'Valor inválido', 'max_digits': 'Valor inválido', 'max_decimal_places': 'Valor inválido'})

    class Meta:
        fields = ['title', 'cost']