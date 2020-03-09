from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from prisoners import models as prisoners_models
from prisons import models as prisons_models
from judges import models as judges_models


class FirstLevel(Sitemap):
    changefreq = 'daily'

    def items(self):
        return [
            'public:homepage', 'public:prisons',
            'public:prisoners', 'public:judges']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        if item != 'public:homepage':
            return 0.8
        else:
            return 0.9


class PrisonersSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return prisoners_models.Prisoner.published_objects.all()

    def location(self, obj):
        return reverse(
            'public:prisoner', kwargs={'pk': obj.id})


class PrisonsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return prisons_models.Prison.published_objects.all()

    def location(self, obj):
        return reverse(
            'public:prison', kwargs={'pk': obj.id})


class JudgesSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return judges_models.Judge.published_objects.all()

    def location(self, obj):
        return reverse(
            'public:judge', kwargs={'pk': obj.id})
