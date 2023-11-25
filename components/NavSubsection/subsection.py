from django_components import component


@component.register("NavSubsection")
class NavSection(component.Component):
    template_name = "NavSubsection/subsection.html"

    def get_context_data(self, title, navSubSection, subSectionSelected, icon, linkTo = None):
        return {
            "title": title,
            "navSubSection": navSubSection,
            "subSectionSelected": subSectionSelected,
            "icon": icon,
            "linkTo": linkTo,
        }
