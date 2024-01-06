from django import forms

class ProductForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, error_messages={'required': 'Campo obrigatório', 'max_length': 'Nome muito grande'})
    description = forms.CharField(max_length=150, required=False, error_messages={'required': 'Campo obrigatório', 'max_length': 'Descrição muito grande'})
    weight = forms.DecimalField(max_digits=10, decimal_places=2, required=True, error_messages={'required': 'Campo obrigatório', 'max_digits': 'Peso muito grande', 'decimal_places': 'Peso Invalido'})
    type = forms.CharField(required=False, error_messages={'required': 'Campo obrigatório'})
    profit_margin = forms.DecimalField(max_digits=3, decimal_places=0, required=True, error_messages={'required': 'Campo obrigatório', 'max_digits': 'Margem de lucro Invalida', 'decimal_places': 'Margem de lucro Invalida'})
    vat = forms.DecimalField(max_digits=3, decimal_places=0, required=True, error_messages={'required': 'Campo obrigatório', 'max_digits': 'IVA Invalido', 'decimal_places': 'IVA Invalido'})
    prop_1 = forms.CharField(required=False, error_messages={'required': 'Necessário selecionar pelo menos um componente'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        props = []
        i = 1
        field_prop_name = 'prop_%s' % (i,)
        field_value_name = 'value_%s' % (i,)

        while self.data.get(field_prop_name) and self.data.get(field_value_name):
            prop = self.data[field_prop_name]
            value = self.data[field_value_name]

            if prop.strip() and value.strip():
                props.append({
                    "prop": prop,
                    "value": value,
                })

                i += 1

                field_prop_name = 'prop_%s' % (i,)
                field_value_name = 'value_%s' % (i,)

        self.cleaned_data['props'] = props

    class Meta:
        fields = ['name', 'description', 'weight', 'type', 'profit_margin', 'vat']