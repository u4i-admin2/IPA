from django.db.models import Q


def update_activities(sender, instance, **kwargs):
    from .models import (
        PrisonerArrest,
        Prisoner
    )
    prisoners_id = PrisonerArrest \
        .objects \
        .filter(
            Q(activity_persecuted_for=instance.id) |
            Q(secondary_activity=instance.id) |
            Q(tertiary_activity=instance.id)) \
        .distinct() \
        .values_list('prisoner_id', flat=True)

    prisoners = Prisoner.objects.filter(id__in=prisoners_id)

    for prisoner in prisoners:
        prisoner.update_summary_fields()
