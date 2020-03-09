from django.apps import AppConfig


class PrisonsConfig(AppConfig):
    name = 'prisons'
    verbose_name = 'Prisons'

    def ready(self):
        import api.search
        import api.viewsets
        import prisons.serializers
        api.viewsets.register(self.name)
        api.search.register(self.get_model('Prison'),
                            prisons.serializers.PrisonSummarySerializer)
