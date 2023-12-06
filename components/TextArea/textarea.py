from django_components import component

@component.register("TextArea")
class NavSection(component.Component):
    template_name = "TextArea/textarea.html"

    def get_context_data(self, name, label, id = None, value = None, error = None):
        return {
            "name": name,
            "label": label,
            "id": id,
            "value": value,
            "error": error,
        }
