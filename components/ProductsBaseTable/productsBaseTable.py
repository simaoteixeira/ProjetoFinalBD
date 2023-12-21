from django_components import component


@component.register("ProductsBaseTable")
class NavSection(component.Component):
    template_name = "ProductsBaseTable/productsBaseTable.html"

    def get_context_data(self, errors, deleteOnSelect = False, canAddProducts = True):
        return {
            "errors": errors,
            "deleteOnSelect": deleteOnSelect,
            "canAddProducts": canAddProducts
        }
