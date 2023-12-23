from django import forms

class ProductForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, error_messages={'required': 'Campo obrigatório', 'max_length': 'Nome muito grande'})
    description = forms.CharField(max_length=150, required=False, error_messages={'required': 'Campo obrigatório', 'max_length': 'Descrição muito grande'})
    weight = forms.DecimalField(max_digits=5, decimal_places=2, required=True, error_messages={'required': 'Campo obrigatório', 'max_digits': 'Peso muito grande', 'decimal_places': 'Peso Invalido'})
    type = forms.CharField(required=True, error_messages={'required': 'Campo obrigatório'})
    profit_margin = forms.DecimalField(max_digits=3, decimal_places=0, required=True, error_messages={'required': 'Campo obrigatório', 'max_digits': 'Margem de lucro Invalida', 'decimal_places': 'Margem de lucro Invalida'})
    vat = forms.DecimalField(max_digits=3, decimal_places=0, required=True, error_messages={'required': 'Campo obrigatório', 'max_digits': 'IVA Invalido', 'decimal_places': 'IVA Invalido'})

    class Meta:
        fields = ['name', 'description', 'weight', 'type', 'profit_margin', 'vat']