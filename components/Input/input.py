from django_components import component

@component.register("Input")
class NavSection(component.Component):
    template_name = "Input/input.html"

    def get_context_data(self, placeholder, inputName, icon = None, type = "text", iconPosition = "left"):
        return {
            "icon": icon,
            "placeholder": placeholder,
            "inputName": inputName,
            "iconPosition": iconPosition,
            "type": type
        }
