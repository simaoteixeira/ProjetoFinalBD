from django_components import component

@component.register("TextArea")
class NavSection(component.Component):
    template_name = "TextArea/textarea.html"

    def get_context_data(self, name, label):
        return {
            "name": name,
            "label": label,
        }
