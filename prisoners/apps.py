from django.apps import AppConfig


class PrisonersConfig(AppConfig):
    name = 'prisoners'
    verbose_name = 'Prisoners'

    def ready(self):
        import api.search
        import api.viewsets
        import prisoners.serializers
        api.viewsets.register(self.name)
        api.search.register(self.get_model('Prisoner'),
                            prisoners.serializers.PrisonerSummarySerializer)
