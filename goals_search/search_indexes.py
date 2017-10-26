from django.apps import apps
from django.db.models import Count
from haystack_es import indexes

Plan = apps.get_registered_model('goals', 'Plan')
Goal = apps.get_registered_model('goals', 'Goal')
Theme = apps.get_registered_model('goals', 'Theme')
Sector = apps.get_registered_model('goals', 'Sector')
Target = apps.get_registered_model('goals', 'Target')
Indicator = apps.get_registered_model('goals', 'Indicator')
Component = apps.get_registered_model('goals', 'Component')


class BaseIndex(indexes.CelerySearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    code = indexes.CharField(model_attr='code', null=True)
    name = indexes.CharField(model_attr='name', null=True)
    description = indexes.CharField(model_attr='description', null=True)
    slug = indexes.CharField(model_attr='slug', null=True)
    image = indexes.CharField(model_attr='image_url', null=True)
    image_small = indexes.CharField(model_attr='image_small_url',
                                    null=True)
    image_medium = indexes.CharField(model_attr='image_medium_url',
                                     null=True)
    image_large = indexes.CharField(model_attr='image_large_url',
                                    null=True)
    api_url = indexes.CharField(model_attr='api_url', null=True)
    extras = indexes.DictField(model_attr='extras', null=True)
    created = indexes.DateTimeField(model_attr='created', null=True)
    last_modified = indexes.DateTimeField(model_attr='last_modified',
                                          null=True)
    object_type = indexes.CharField(faceted=True, null=True)

    def get_updated_field(self):
        return 'last_modified'

    def prepare_object_type(self, obj):
        return self.get_model().__name__.lower()


class SectorIndex(BaseIndex, indexes.Indexable):
    parent = indexes.IntegerField(model_attr='parent_id', null=True,
                                  faceted=True)
    parent_name = indexes.CharField(model_attr='parent__name', null=True,
                                    faceted=True)
    level = indexes.IntegerField(model_attr='level', null=True, faceted=True)
    themes_ids = indexes.MultiValueField(faceted=True, null=True)
    themes_codes = indexes.MultiValueField(
        model_attr='themes_codes', faceted=True, null=True)
    themes_names = indexes.MultiValueField(
        model_attr='themes_names', faceted=True, null=True)
    plans_ids = indexes.MultiValueField(
        model_attr='plans_ids', faceted=True, null=True)
    plans_codes = indexes.MultiValueField(
        model_attr='plans_codes', faceted=True, null=True)
    plans_names = indexes.MultiValueField(
        model_attr='plans_names', faceted=True, null=True)

    def get_model(self):
        return Sector

    def prepare_indicators(self, obj):
        return list(obj.themes.values_list('id', flat=True))


class PlanIndex(BaseIndex, indexes.Indexable):
    caption = indexes.CharField(model_attr='caption', null=True)

    def get_model(self):
        return Plan


class ThemeIndex(BaseIndex, indexes.Indexable):
    caption = indexes.CharField(model_attr='caption', null=True)
    plan = indexes.IntegerField(model_attr='plan_id',
                                null=True, faceted=True)
    plan_code = indexes.CharField(model_attr='plan_code',
                                  null=True, faceted=True)
    plan_name = indexes.CharField(model_attr='plan_name',
                                  null=True, faceted=True)

    def get_model(self):
        return Theme


class GoalIndex(ThemeIndex):

    def get_model(self):
        return Goal


class TargetIndex(BaseIndex, indexes.Indexable):
    plan = indexes.IntegerField(model_attr='plan_id',
                                null=True, faceted=True)
    plan_code = indexes.CharField(model_attr='plan_code',
                                  null=True, faceted=True)
    plan_name = indexes.CharField(model_attr='plan_name',
                                  null=True, faceted=True)
    goal = indexes.IntegerField(model_attr='goal_id',
                                null=True, faceted=True)
    goal_code = indexes.CharField(model_attr='goal_code',
                                  null=True, faceted=True)
    goal_name = indexes.CharField(model_attr='goal_name',
                                  null=True, faceted=True)
    plan_id = indexes.IntegerField(model_attr='plan_id',
                                   null=True, faceted=True)

    def get_model(self):
        return Target


class IndicatorIndex(TargetIndex, indexes.Indexable):
    theme = indexes.IntegerField(model_attr='theme_id',
                                 null=True, faceted=True)
    theme_name = indexes.CharField(model_attr='theme_name',
                                   null=True, faceted=True)
    sector = indexes.IntegerField(model_attr='sector_id',
                                  null=True, faceted=True)
    sector_name = indexes.CharField(model_attr='sector_name',
                                    null=True, faceted=True)
    sector_code = indexes.CharField(model_attr='sector_code',
                                    null=True, faceted=True)
    sectors_names = indexes.MultiValueField(
        model_attr='sectors_names', faceted=True, null=True)
    sectors_ids = indexes.MultiValueField(
        model_attr='sectors_ids', faceted=True, null=True)
    sectors_codes = indexes.MultiValueField(
        model_attr='sectors_codes', faceted=True, null=True)
    sector_type_code = indexes.CharField(
        model_attr='sector_type_code', faceted=True, null=True)
    sector_type_name = indexes.CharField(
        model_attr='sector_type_name', faceted=True, null=True)
    root_sector_id = indexes.IntegerField(model_attr='root_sector_id',
                                          null=True, faceted=True)
    root_sector_code = indexes.CharField(model_attr='root_sector_code',
                                         null=True, faceted=True)
    root_sector_name = indexes.CharField(model_attr='root_sector_name',
                                         null=True, faceted=True)
    target = indexes.IntegerField(model_attr='target_id',
                                  null=True, faceted=True)
    target_code = indexes.CharField(model_attr='target_code',
                                    null=True, faceted=True)
    target_name = indexes.CharField(model_attr='target_name',
                                    null=True, faceted=True)
    goal_id = indexes.IntegerField(model_attr='goal_id',
                                   null=True, faceted=True)
    plan_id = indexes.IntegerField(model_attr='plan_id',
                                   null=True, faceted=True)
    progress_count = indexes.IntegerField(null=True)

    def get_model(self):
        return Indicator

    def index_queryset(self, using=None):
        return self.get_model().objects.annotate(
            progress_count=Count('components__progress'))

    def prepare_progress_count(self, obj):
        return obj.get_progress_count()


class ComponentIndex(BaseIndex, indexes.Indexable):
    indicators = indexes.MultiValueField(faceted=True, null=True)
    indicators_names = indexes.MultiValueField(
        model_attr='indicators_names', faceted=True, null=True)
    indicators_codes = indexes.MultiValueField(
        model_attr='indicators_codes', faceted=True, null=True)
    targets_ids = indexes.MultiValueField(
        model_attr='targets_ids', faceted=True, null=True)
    targets_codes = indexes.MultiValueField(
        model_attr='targets_codes', faceted=True, null=True)
    targets_names = indexes.MultiValueField(
        model_attr='targets_names', faceted=True, null=True)
    goals_ids = indexes.MultiValueField(
        model_attr='goals_ids', faceted=True, null=True)
    goals_codes = indexes.MultiValueField(
        model_attr='goals_codes', faceted=True, null=True)
    goals_names = indexes.MultiValueField(
        model_attr='goals_names', faceted=True, null=True)
    plans_ids = indexes.MultiValueField(
        model_attr='plans_ids', faceted=True, null=True)
    plans_codes = indexes.MultiValueField(
        model_attr='plans_codes', faceted=True, null=True)
    plans_names = indexes.MultiValueField(
        model_attr='plans_names', faceted=True, null=True)
    agency = indexes.CharField(model_attr='agency',
                               null=True, faceted=True)
    data_source = indexes.CharField(model_attr='data_source',
                                    null=True, faceted=True)
    stats_available = indexes.BooleanField(model_attr='stats_available',
                                           null=True, faceted=True)
    progress_count = indexes.IntegerField(null=True)

    def get_model(self):
        return Component

    def index_queryset(self, using=None):
        return self.get_model().objects.annotate(
            progress_count=Count('progress'))

    def prepare_indicators(self, obj):
        return list(obj.indicators.values_list('id', flat=True))

    def prepare_progress_count(self, obj):
        return obj.get_progress_count()
