from django.apps import AppConfig


class CoreTypesConfig(AppConfig):
    name = 'core_types'
    verbose_name = "Editable Categories"

    def ready(self):
        import api.viewsets
        api.viewsets.register(self.name)
