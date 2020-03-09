from model_mommy import mommy

import prisoners.models
import judges.models
import prisons.models
import core_types.models


def generic_teardown():
    judges.models.Judge.objects.all().delete()
    judges.models.BehaviourType.objects.all().delete()
    prisons.models.Prison.objects.all().delete()
    prisoners.models.ChargedWith.objects.all().delete()
    prisoners.models.PrisonTreatment.objects.all().delete()
    prisoners.models.PrisonerSentence.objects.all().delete()
    prisoners.models.PrisonerDetention.objects.all().delete()
    prisoners.models.PrisonerArrest.objects.all().delete()
    prisoners.models.ActivityPersecutedFor.objects.all().delete()
    prisoners.models.SentenceBehaviour.objects.all().delete()
    core_types.models.Religion.objects.all().delete()
    core_types.models.Ethnicity.objects.all().delete()
    prisoners.models.Prisoner.objects.all().delete()


def fixtures_for_prison_view(cls):
    cls.religion = mommy.make('core_types.Religion', name='wobbles')
    cls.ethnicity = mommy.make('core_types.Ethnicity', name='bobbles')

    cls.religionB = mommy.make('core_types.Religion', name='nibbles')
    cls.ethnicityB = mommy.make('core_types.Ethnicity', name='nobbles')

    cls.prison = mommy.make('prisons.Prison', name='PrisonA', is_published=True)
    cls.prisonB = mommy.make('prisons.Prison', name='PrisonB', is_published=True)
    cls.prisonC = mommy.make('prisons.Prison', name='PrisonC', is_published=False)
    cls.prisonD = mommy.make('prisons.Prison', name='PrisonD', is_published=True)

    cls.treatmentA = mommy.make('prisoners.PrisonTreatment', name='Treatment A')
    cls.treatmentB = mommy.make('prisoners.PrisonTreatment', name='Treatment B')
    cls.treatmentC = mommy.make('prisoners.PrisonTreatment', name='Treatment C')

    cls.activityA = mommy.make('prisoners.ActivityPersecutedFor', name='Activity A')
    cls.activityB = mommy.make('prisoners.ActivityPersecutedFor', name='Activity B')
    cls.activityC = mommy.make('prisoners.ActivityPersecutedFor', name='Activity C')

    cls.judgeA = mommy.make('judges.Judge', surname='JudgeA')

    cls.chargeA = mommy.make('prisoners.ChargedWith', name='Charge A')
    cls.chargeB = mommy.make('prisoners.ChargedWith', name='Charge B')
    cls.chargeC = mommy.make('prisoners.ChargedWith', name='Charge C')

    cls.prisonerA = prisoners.models.Prisoner.objects.create(
        forename='flib', surname='flob', gender="M",
        is_published=True, religion=cls.religion)

    cls.prisonerB = prisoners.models.Prisoner.objects.create(
        forename='blib', surname='blob', gender="F",
        is_published=True, ethnicity=cls.ethnicity)

    cls.prisonerD = prisoners.models.Prisoner.objects.create(
        is_published=True, gender="M", surname="Mr D",
        religion=cls.religionB, ethnicity=cls.ethnicityB)

    cls.prisonerE = prisoners.models.Prisoner.objects.create(
        is_published=True, gender="F", religion=cls.religion,
        surname="Mr E", ethnicity=cls.ethnicityB)

    cls.prisonerF = prisoners.models.Prisoner.objects.create(
        is_published=True, gender="M", religion=cls.religionB,
        surname="Mr F", ethnicity=cls.ethnicity)

    cls.prisonerC = prisoners.models.Prisoner.objects.create(
        latest_prison_name_en='PrisonA', is_published=False)

    # prisoner A
    cls.prisonerArrestA1 = prisoners.models.PrisonerArrest.objects.create(
        prisoner=cls.prisonerA,
        arrest_year=2012,
        arrest_month=10,
        arrest_day=10,
        is_published=True)
    cls.prisonerArrestA1.charged_with.add(cls.chargeA)
    cls.prisonerArrestA2 = prisoners.models.PrisonerArrest.objects.create(
        prisoner=cls.prisonerA,
        arrest_year=2014,
        arrest_month=11,
        arrest_day=11,
        is_published=True,
        activity_persecuted_for=cls.activityA)
    cls.prisonerArrestA2.charged_with.add(cls.chargeB)

    cls.prisonerSentence = prisoners.models.PrisonerSentence.objects.create(
        arrest=cls.prisonerArrestA2,
        judge=cls.judgeA,
        is_published=True)
    cls.prisonerDetentionA = prisoners.models.PrisonerDetention.objects.create(
        prison=cls.prison,
        arrest=cls.prisonerArrestA1,
        detention_year=2015,
        detention_month=12,
        detention_day=12,
        is_published=True)
    cls.prisonerDetentionA.treatment.add(cls.treatmentC)
    cls.prisonerDetentionA2 = prisoners.models.PrisonerDetention.objects.create(
        prison=cls.prison,
        arrest=cls.prisonerArrestA2,
        detention_year=2014,
        detention_month=11,
        detention_day=11,
        is_published=True)
    cls.prisonerDetentionA2.treatment.add(cls.treatmentB)
    cls.prisonerDetentionA2.treatment.add(cls.treatmentA)

    # prisoner B
    cls.prisonerArrestB1 = prisoners.models.PrisonerArrest.objects.create(
        prisoner=cls.prisonerB,
        arrest_year=2014,
        arrest_month=12,
        arrest_day=12,
        is_published=True,
        activity_persecuted_for=cls.activityA)
    cls.prisonerArrestB1.charged_with.add(cls.chargeC)
    cls.prisonerArrestB1.charged_with.add(cls.chargeB)
    cls.prisonerArrestB2 = prisoners.models.PrisonerArrest.objects.create(
        prisoner=cls.prisonerB,
        arrest_year=2013,
        arrest_month=10,
        arrest_day=10,
        is_published=True)
    cls.prisonerArrestB2.charged_with.add(cls.chargeA)
    cls.prisonerDetentionB1 = prisoners.models.PrisonerDetention.objects.create(
        prison=cls.prison,
        arrest=cls.prisonerArrestB1,
        detention_year=2015,
        detention_month=11,
        detention_day=11,
        is_published=True)
    cls.prisonerDetentionB1.treatment.add(cls.treatmentC)
    cls.prisonerDetentionB1.treatment.add(cls.treatmentA)
    cls.prisonerDetentionB2 = prisoners.models.PrisonerDetention.objects.create(
        prison=cls.prison,
        arrest=cls.prisonerArrestB1,
        detention_year=2012,
        detention_month=10,
        detention_day=10,
        is_published=True)
    cls.prisonerDetentionB2.treatment.add(cls.treatmentC)

    # prisoner D
    cls.prisonerArrestD1 = prisoners.models.PrisonerArrest.objects.create(
        prisoner=cls.prisonerD,
        arrest_year=2012,
        arrest_month=10,
        arrest_day=10,
        is_published=True)
    cls.prisonerArrestD1.charged_with.add(cls.chargeC)
    cls.prisonerArrestD1.charged_with.add(cls.chargeA)

    cls.prisonerDetentionD1 = prisoners.models.PrisonerDetention.objects.create(
        prison=cls.prisonD,
        arrest=cls.prisonerArrestD1,
        detention_year=2015,
        detention_month=11,
        detention_day=11,
        is_published=True)
    cls.prisonerDetentionD1.treatment.add(cls.treatmentA)
    cls.prisonerDetentionD1.treatment.add(cls.treatmentB)

    # prisoner E
    cls.prisonerArrestE1 = prisoners.models.PrisonerArrest.objects.create(
        prisoner=cls.prisonerE,
        arrest_year=2012,
        arrest_month=10,
        arrest_day=10,
        is_published=True)
    cls.prisonerArrestE1.charged_with.add(cls.chargeA)
    cls.prisonerArrestE1.charged_with.add(cls.chargeB)

    cls.prisonerDetentionE1 = prisoners.models.PrisonerDetention.objects.create(
        prison=cls.prisonD,
        arrest=cls.prisonerArrestE1,
        detention_year=2015,
        detention_month=11,
        detention_day=11,
        is_published=True)
    cls.prisonerDetentionE1.treatment.add(cls.treatmentC)
    cls.prisonerDetentionE1.treatment.add(cls.treatmentA)

    # prisoner F
    cls.prisonerArrestF1 = prisoners.models.PrisonerArrest.objects.create(
        prisoner=cls.prisonerF,
        arrest_year=2012,
        arrest_month=10,
        arrest_day=10,
        is_published=True,
        activity_persecuted_for=cls.activityC)
    cls.prisonerArrestF1.charged_with.add(cls.chargeB)
    cls.prisonerArrestF1.charged_with.add(cls.chargeC)

    cls.prisonerDetentionF1 = prisoners.models.PrisonerDetention.objects.create(
        prison=cls.prisonB,
        arrest=cls.prisonerArrestF1,
        detention_year=2015,
        detention_month=11,
        detention_day=11,
        is_published=True)
    cls.prisonerDetentionF1.treatment.add(cls.treatmentC)
    cls.prisonerDetentionF1.treatment.add(cls.treatmentB)


def fixtures_for_judge_view(cls):
    cls.religionA = mommy.make('core_types.Religion', name='religionA')
    cls.ethnicityA = mommy.make('core_types.Ethnicity', name='ethnicityA')

    cls.chargeA = mommy.make('prisoners.ChargedWith', name='Charge A')
    cls.chargeB = mommy.make('prisoners.ChargedWith', name='Charge B')
    cls.chargeC = mommy.make('prisoners.ChargedWith', name='Charge C')

    cls.judge = mommy.make('judges.Judge', surname='JudgeA', is_published=True)
    cls.judgeB = mommy.make('judges.Judge', surname='JudgeB', is_published=True)
    cls.judgeC = mommy.make('judges.Judge', surname='JudgeC', is_published=True)
    cls.judgeUnpublished = mommy.make('judges.Judge')

    cls.activityA = mommy.make('prisoners.ActivityPersecutedFor', name='Activity A')
    cls.activityB = mommy.make('prisoners.ActivityPersecutedFor', name='Activity B')
    cls.activityC = mommy.make('prisoners.ActivityPersecutedFor', name='Activity C')

    cls.treatmentA = mommy.make('prisoners.PrisonTreatment', name='Treatment A')

    cls.judgeBehaviourA = mommy.make(
        'judges.BehaviourType', name='Behaviour A', is_published=True)
    cls.judgeBehaviourB = mommy.make(
        'judges.BehaviourType', name='Behaviour B', is_published=True)
    cls.judgeBehaviourC = mommy.make(
        'judges.BehaviourType', name='Behaviour C', is_published=True)

    cls.prisonerA = prisoners.models.Prisoner.objects.create(
        is_published=True, religion=cls.religionA, ethnicity=cls.ethnicityA)
    cls.prisonerB = prisoners.models.Prisoner.objects.create(
        is_published=True, religion=cls.religionA, ethnicity=cls.ethnicityA)

    # prisoner A
    # prisA -> arrestA1 (chargeC,B,A activityA,B) -> sentenceA, sentenceB (behaviour A, behaviour B)
    # months = 8, years = 28
    cls.prisonerArrestA1 = prisoners.models.PrisonerArrest.objects.create(
        prisoner=cls.prisonerA,
        arrest_year=2009,
        arrest_month=03,
        arrest_day=03,
        activity_persecuted_for=cls.activityA,
        is_published=True)
    cls.prisonerArrestA1.charged_with.add(cls.chargeC)
    cls.prisonerArrestA1.charged_with.add(cls.chargeA)

    cls.prisonerArrestA2 = prisoners.models.PrisonerArrest.objects.create(
        prisoner=cls.prisonerA,
        arrest_year=2014,
        arrest_month=07,
        arrest_day=07,
        activity_persecuted_for=cls.activityB,
        is_published=True)
    cls.prisonerArrestA2.charged_with.add(cls.chargeB)

    cls.prisonerSentenceA = prisoners.models.PrisonerSentence.objects.create(
        arrest=cls.prisonerArrestA1,
        judge=cls.judge,
        sentence_months=05,
        number_of_lashes=100,
        death_penalty=True,
        sentence_years=10,
        is_published=True)
    cls.prisonerSentenceA2 = prisoners.models.PrisonerSentence.objects.create(
        arrest=cls.prisonerArrestA2,
        judge=cls.judge,
        number_of_lashes=100,
        death_penalty=True,
        sentence_months=03,
        sentence_years=18,
        is_published=True)
    prisoners.models.SentenceBehaviour.objects.create(
        sentence=cls.prisonerSentenceA,
        behaviour_type=cls.judgeBehaviourA,
        is_published=True)
    prisoners.models.SentenceBehaviour.objects.create(
        sentence=cls.prisonerSentenceA2,
        behaviour_type=cls.judgeBehaviourB,
        is_published=True)

    cls.prisonerDetentionA1 = prisoners.models.PrisonerDetention.objects.create(
        is_published=True,
        arrest=cls.prisonerArrestA1)
    cls.prisonerDetentionA1.treatment.add(cls.treatmentA)

    cls.prisonerDetentionA2 = prisoners.models.PrisonerDetention.objects.create(
        arrest=cls.prisonerArrestA2,
        is_published=True)
    cls.prisonerDetentionA2.treatment.add(cls.treatmentA)

    cls.prisonerSentenceA3 = prisoners.models.PrisonerSentence.objects.create(
        arrest=cls.prisonerArrestA2,
        judge=cls.judgeC,
        sentence_months=10,
        sentence_years=8,
        is_published=True,
        death_penalty=True,
        number_of_lashes=27)
    prisoners.models.SentenceBehaviour.objects.create(
        sentence=cls.prisonerSentenceA3,
        behaviour_type=cls.judgeBehaviourA,
        is_published=True)

    # prisoner B
    # prisB -> arrestB1, B2 (chargeA,B/B, activityC/B) -> sentenceB, sentenceB2, sentenceB3 (C, C, A, A)
    # months = 25 years = 24
    cls.prisonerArrestB1 = prisoners.models.PrisonerArrest.objects.create(
        prisoner=cls.prisonerB,
        arrest_year=2015,
        arrest_month=07,
        arrest_day=21,
        activity_persecuted_for=cls.activityC,
        is_published=True)
    cls.prisonerArrestB1.charged_with.add(cls.chargeA)
    cls.prisonerArrestB1.charged_with.add(cls.chargeB)

    cls.prisonerArrestB2 = prisoners.models.PrisonerArrest.objects.create(
        prisoner=cls.prisonerB,
        arrest_year=2013,
        arrest_month=05,
        arrest_day=24,
        activity_persecuted_for=cls.activityB,
        is_published=True)
    cls.prisonerArrestB2.charged_with.add(cls.chargeB)

    cls.prisonerSentenceB1 = prisoners.models.PrisonerSentence.objects.create(
        arrest=cls.prisonerArrestB1,
        judge=cls.judge,
        sentence_months=03,
        sentence_years=2,
        is_published=True)
    cls.prisonerSentenceB2 = prisoners.models.PrisonerSentence.objects.create(
        arrest=cls.prisonerArrestB1,
        judge=cls.judge,
        sentence_months=11,
        sentence_years=18,
        is_published=True)

    prisoners.models.SentenceBehaviour.objects.create(
        sentence=cls.prisonerSentenceB1,
        behaviour_type=cls.judgeBehaviourA,
        is_published=True)
    prisoners.models.SentenceBehaviour.objects.create(
        sentence=cls.prisonerSentenceB2,
        behaviour_type=cls.judgeBehaviourC,
        is_published=True)

    cls.prisonerSentenceB3 = prisoners.models.PrisonerSentence.objects.create(
        arrest=cls.prisonerArrestB2,
        judge=cls.judge,
        sentence_months=11,
        sentence_years=4,
        is_published=True)
    prisoners.models.SentenceBehaviour.objects.create(
        sentence=cls.prisonerSentenceB3,
        behaviour_type=cls.judgeBehaviourA,
        is_published=True)
    prisoners.models.SentenceBehaviour.objects.create(
        sentence=cls.prisonerSentenceB3,
        behaviour_type=cls.judgeBehaviourC,
        is_published=True)
