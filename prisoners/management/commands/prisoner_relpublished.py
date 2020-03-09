from django.core.management.base import BaseCommand

"""
PRISONER related models

prisoner.models.PrisonerQuote
prisoner.models.PrisonerFile
prisoner.models.PrisonerAffiliation
prisoner.models.PrisonerRelationship
prisoner.models.DetentionStatus
prisoner.models.PrisonerArrest
prisoner.models.ActivityPersecutedFor
prisoner.models.CaseId
prisoner.models.ChargedWith
prisoner.models.DomesticLawViolated
prisoner.models.InternationalLawViolated
prisoner.models.PrisonerSentence
prisoner.models.PrisonTreatment
prisoner.models.PrisonerTimeline
prisoner.models.PrisonerSource

judges.models.CourtAndBranch
judges.models.BehaviourType
judges.models.SentenceType

core_types.models.Country
core_types.models.Religion
core_types.models.Ethnicity
core_types.models.City
core_types.models.Province

DO NOT update main models
prisons.models.Prison
judges.models.Judge

prisonerdetention !!!!

"""
import prisoners.models as prisoners_models
import judges.models as judges_models
import core_types.models as core_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        prisoners_models.PrisonerQuote.objects.all().update(is_published=True)
        prisoners_models.PrisonerFile.objects.all().update(is_published=True)
        prisoners_models.PrisonerAffiliation.objects.all().update(is_published=True)
        prisoners_models.PrisonerRelationship.objects.all().update(is_published=True)
        prisoners_models.DetentionStatus.objects.all().update(is_published=True)
        prisoners_models.PrisonerArrest.objects.all().update(is_published=True)
        prisoners_models.ActivityPersecutedFor.objects.all().update(is_published=True)
        prisoners_models.CaseId.objects.all().update(is_published=True)
        prisoners_models.ChargedWith.objects.all().update(is_published=True)
        prisoners_models.DomesticLawViolated.objects.all().update(is_published=True)
        prisoners_models.InternationalLawViolated.objects.all().update(is_published=True)
        prisoners_models.PrisonerSentence.objects.all().update(is_published=True)
        prisoners_models.PrisonTreatment.objects.all().update(is_published=True)
        prisoners_models.PrisonerTimeline.objects.all().update(is_published=True)
        prisoners_models.PrisonerSource.objects.all().update(is_published=True)
        prisoners_models.PrisonerDetention.objects.all().update(is_published=True)
        # prisoners_models.PrisonerComment.objects.all().update(is_published=True)
        print('Prisoner related models updated')
        judges_models.CourtAndBranch.objects.all().update(is_published=True)
        judges_models.BehaviourType.objects.all().update(is_published=True)
        judges_models.SentenceType.objects.all().update(is_published=True)
        print('Prisoner related Judge models updated')
        core_models.Country.objects.all().update(is_published=True)
        core_models.Religion.objects.all().update(is_published=True)
        core_models.Ethnicity.objects.all().update(is_published=True)
        core_models.City.objects.all().update(is_published=True)
        core_models.Province.objects.all().update(is_published=True)
        print('Prisoner related Core models updated')
