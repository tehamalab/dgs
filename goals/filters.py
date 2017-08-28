import django_filters
from .models import (Plan, Goal, Theme, Sector, Target, Indicator, Component,
                     Progress, Area, AreaType)


class AreaFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    type = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Area
        fields = ['code', 'level']


class PlanFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Plan
        fields = ['code']


class GoalFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    description = django_filters.CharFilter(lookup_expr='icontains')
    plan_code = django_filters.CharFilter(name='plan__code')

    class Meta:
        model = Goal
        fields = ['plan', 'code']


class ThemeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    description = django_filters.CharFilter(lookup_expr='icontains')
    plan_code = django_filters.CharFilter(name='plans__code')

    class Meta:
        model = Theme
        fields = ['plans', 'code']


class SectorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Sector
        fields = ['parent', 'theme']


class TargetFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Target
        fields = ['goal', 'code']


class IndicatorFilter(django_filters.FilterSet):
    goal = django_filters.ModelChoiceFilter(name='target__goal',
                                            queryset=Goal.objects.all())
    description = django_filters.CharFilter(lookup_expr='icontains')
    data_source = django_filters.CharFilter(lookup_expr='icontains')
    agency = django_filters.CharFilter(lookup_expr='iexact')
    progress_count = django_filters.NumberFilter(lookup_expr='gte')

    class Meta:
        model = Indicator
        fields = ['target', 'theme', 'sector', 'code']


class ComponentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    goal = django_filters.ModelChoiceFilter(
        name='indicators__target__goal', queryset=Goal.objects.all())
    progress_count = django_filters.NumberFilter(lookup_expr='gte')

    class Meta:
        model = Component
        fields = ['indicators', 'code', 'stats_available']


class ProgressFilter(django_filters.FilterSet):
    indicator = django_filters.ModelChoiceFilter(
        name='component__indicators', queryset=Indicator.objects.all())
    target = django_filters.ModelChoiceFilter(
        name='component__indicators__target',
        queryset=Target.objects.all())
    area_code = django_filters.CharFilter(name='area__code')
    area_type = django_filters.ModelChoiceFilter(
        name='area__type', queryset=AreaType.objects.all())
    area_type_code = django_filters.CharFilter(name='area__type__code')

    class Meta:
        model = Progress
        fields = {
            'component': ['exact'],
            'area': ['exact'],
            'year': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'fiscal_year': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'value': ['exact', 'lt', 'lte', 'gt', 'gte']
        }
