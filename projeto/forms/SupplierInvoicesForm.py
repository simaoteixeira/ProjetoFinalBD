import datetime

from django import forms

from projeto.utils import compareDates


class SupplierInvoicesForm(forms.Form):
    supplier = forms.IntegerField(required=True, error_messages={'required': 'Campo obrigatório'})
    invoice_id = forms.CharField(required=True, error_messages={'required': 'Campo obrigatório'})
    invoice_date = forms.DateField(required=True, error_messages={'required': 'Campo obrigatório'})
    expire_date = forms.DateField(required=True, error_messages={'required': 'Campo obrigatório'})
    obs = forms.CharField(required=False, max_length=500, error_messages={'max_length': 'Máximo de 500 caracteres'})
    material_receipt_1 = forms.IntegerField(required=True, error_messages={'required': 'Necessário selecionar pelo menos uma recessão de material'})
    product_1 = forms.CharField(required=True, error_messages={'required': 'Necessário selecionar pelo menos um componente'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # field_name = 'product_%s' % (1,)
        # self.fields[field_name] = forms.CharField(required=False)

    def clean(self):
        products = []
        material_receipts = []
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

            products[products.index(product_id)] = {
                "id": product_id,
                "quantity": quantity,
                "price_base": price_base,
                "vat": vat,
                "discount": discount,
            }

        self.cleaned_data['products'] = products

        i = 1
        field_name = 'material_receipt_%s' % (i,)

        while self.data.get(field_name):
            material_receipt = self.data[field_name]
            if material_receipt in material_receipts:
                self.add_error(field_name, 'Duplicate')
            else:
                material_receipts.append(material_receipt)

            i += 1
            field_name = 'material_receipt_%s' % (i,)

        self.cleaned_data['material_receipts'] = material_receipts

        invoice_date = self.data['invoice_date']
        expire_date = self.data['expire_date']

        if not invoice_date:
            self.add_error('invoice_date', 'Campo obrigatório')
            return

        if not expire_date:
            self.add_error('expire_date', 'Campo obrigatório')
            return

        if not compareDates(expire_date, str(datetime.date.today())):
            self.add_error('expire_date', 'Data deve ser posterior à data atual')

        if compareDates(invoice_date, expire_date):
            self.add_error('invoice_date', 'Data deve ser anterior à data de vencimento')

    def get_material_receipts_fields(self):
        for field_name in self.fields:
            if field_name.startswith('material_receipt_'):
                yield self[field_name]


    class Meta:
        fields = ['supplier', 'invoice_id', 'invoice_date', 'expire_date', 'obs']