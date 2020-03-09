from django.apps import AppConfig


class JudgesConfig(AppConfig):
    name = 'judges'
    verbose_name = 'Judges'

    def ready(self):
        import api.search
        import api.viewsets
        import judges.serializers
        api.viewsets.register(self.name)
        api.search.register(self.get_model('Judge'),
                            judges.serializers.JudgeSummarySerializer)
