from django import forms
from django.core.validators import RegexValidator


class SuppliersForm(forms.Form):
    name = forms.CharField(max_length=100, required=True,
                           error_messages={'required': 'Campo obrigatório', 'max_length': 'Nome muito longo'})
    email = forms.EmailField(required=True,
                             error_messages={'required': 'Campo obrigatório', 'invalid': 'Email inválido'})
    phone = forms.CharField(max_length=9, required=True,
                            error_messages={'required': 'Campo obrigatório', 'max_length': 'Telefone Invalido'})
    nif = forms.CharField(max_length=9, required=True,
                          error_messages={'required': 'Campo obrigatório', 'max_length': 'NIF Invalido'})
    address = forms.CharField(max_length=100, required=True,
                              error_messages={'required': 'Campo obrigatório', 'max_length': 'Morada muito longa'})
    locality = forms.CharField(max_length=50, required=True,
                               error_messages={'required': 'Campo obrigatório', 'max_length': 'Localidade muito longa'})
    postal_code = forms.CharField(required=True, error_messages={'required': 'Obrigatório'},
                                  validators=[RegexValidator(
                                      regex=r'^(^[0-9]{4}(?:-[0-9]{3})$|^$)',
                                      message='Invalido',
                                  )])

    class Meta:
        fields = ['name', 'email', 'phone', 'nif', 'address', 'locality', 'postal_code']