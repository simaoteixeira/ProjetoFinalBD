from django import forms


class MaterialReceiptsForm(forms.Form):
    supplier = forms.IntegerField(required=True, error_messages={'required': 'Campo obrigatório'})
    purchasing_order = forms.IntegerField(required=True, error_messages={'required': 'Campo obrigatório'})
    n_delivery_note = forms.CharField(required=True, error_messages={'required': 'Campo obrigatório'})
    obs = forms.CharField(required=False, max_length=500, error_messages={'max_length': 'Máximo de 500 caracteres'})
    product_1 = forms.CharField(required=True, error_messages={'required': 'Necessário selecionar pelo menos um componente'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # field_name = 'product_%s' % (1,)
        # self.fields[field_name] = forms.CharField(required=False)

    def clean(self):
        products = []
        i = 1
        field_name = 'product_%s' % (i,)

        while self.data.get(field_name):
            product = self.data[field_name]
            if product in products:
                self.add_error(field_name, 'Duplicate')
            else:
                products.append(product)

            i += 1
            field_name = 'product_%s' % (i,)

        for product_id in products:
            quantity = self.data["quantity-" + str(product_id)]
            price_base = self.data["unit_value-" + str(product_id)]
            vat = self.data["IVA-" + str(product_id)]
            discount = self.data["discount-" + str(product_id)]
            warehouse = self.data["warehouse-" + str(product_id)]

            products[products.index(product_id)] = {
                "id": product_id,
                "quantity": quantity,
                "price_base": price_base,
                "vat": vat,
                "discount": discount,
                "warehouse": warehouse
            }

        self.cleaned_data['products'] = products

    def get_products_fields(self):
        for field_name in self.fields:
            if field_name.startswith('product_'):
                yield self[field_name]

    class Meta:
        fields = ['supplier', 'purchasing_order', 'n_delivery_note', 'obs']