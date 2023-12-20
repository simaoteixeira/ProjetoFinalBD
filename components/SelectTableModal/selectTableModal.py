from django_components import component


@component.register("SelectTableModal")
class SelectTableModal(component.Component):
    template_name = "SelectTableModal/selectTableModal.html"

    def get_context_data(self, id, title, table):
        return {
            "id": id,
            "title": title,
            "table": table,
        }
