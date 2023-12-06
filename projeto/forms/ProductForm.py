from django import forms

class ProductForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, error_messages={'required': 'Campo obrigatório', 'max_length': 'Nome muito grande'})
    description = forms.CharField(max_length=150, required=True, error_messages={'required': 'Campo obrigatório', 'max_length': 'Descrição muito grande'})
    weight = forms.DecimalField(max_digits=5, decimal_places=2, required=True, error_messages={'required': 'Campo obrigatório', 'max_digits': 'Peso muito grande', 'decimal_places': 'Peso Invalido'})
    #type =
    profit_margin = forms.DecimalField(max_digits=3, decimal_places=0, required=True, error_messages={'required': 'Campo obrigatório', 'max_digits': 'Margem de lucro Invalida', 'decimal_places': 'Margem de lucro Invalida'})
    vat = forms.DecimalField(max_digits=3, decimal_places=0, required=True, error_messages={'required': 'Campo obrigatório', 'max_digits': 'IVA Invalido', 'decimal_places': 'IVA Invalido'})
    price_cost = forms.DecimalField(max_digits=5, decimal_places=2, required=True, error_messages={'required': 'Campo obrigatório', 'max_digits': 'Preço de custo Invalido', 'decimal_places': 'Preço de custo Invalido'})
    price_base = forms.DecimalField(max_digits=5, decimal_places=2, required=True, error_messages={'required': 'Campo obrigatório', 'max_digits': 'Preço base Invalido', 'decimal_places': 'Preço base Invalido'})
    pvp = forms.DecimalField(max_digits=5, decimal_places=2, required=True, error_messages={'required': 'Campo obrigatório', 'max_digits': 'PVP Invalido', 'decimal_places': 'PVP Invalido'})

    class Meta:
        fields = ['name', 'description', 'weight', 'profit_margin', 'vat', 'price_cost', 'price_base', 'pvp']