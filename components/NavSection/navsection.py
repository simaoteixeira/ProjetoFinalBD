from django_components import component


@component.register("NavSection")
class NavSection(component.Component):
    template_name = "NavSection/navsection.html"

    def get_context_data(self, title, navSection, sectionSelected, icon):
        return {
            "title": title,
            "navSection": navSection,
            "sectionSelected": sectionSelected,
            "icon": icon
        }
