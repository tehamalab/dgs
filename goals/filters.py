import django_filters
from .models import (Plan, Goal, Target, Indicator, Component, Progress,
                     Area)


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
    sort = django_filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('name', 'name'),
            ('code', 'code'),
        ))

    class Meta:
        model = Goal
        fields = ['code']


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

    class Meta:
        model = Indicator
        fields = ['target', 'code', 'stats_available']


class ComponentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    goal = django_filters.ModelChoiceFilter(
        name='indicators__target__goal', queryset=Goal.objects.all())

    class Meta:
        model = Component
        fields = ['indicators', 'code']


class ProgressFilter(django_filters.FilterSet):
    sort = django_filters.OrderingFilter(
        fields=(
            ('year', 'year'),
            ('component', 'component'),
            ('area', 'area'),
            ('value', 'velue'),
            ('created', 'created'),
            ('last_modified', 'last_modified'),
        ))

    class Meta:
        model = Progress
        fields = {
            'component': ['exact'],
            'area': ['exact'],
            'area__code': ['exact'],
            'year': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'value': ['exact', 'lt', 'lte', 'gt', 'gte']
        }
