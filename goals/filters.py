import django_filters
from .models import Goal, Target, Indicator, Component, Progress, Area


class AreaFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    type = django_filters.CharFilter(lookup_expr='iexact')
    sort = django_filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('name', 'name'),
            ('code', 'code'),
            ('type', 'type'),
        ))

    class Meta:
        model = Area
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
    description = django_filters.CharFilter(lookup_expr='icontains')
    target_description = django_filters.CharFilter(
        lookup_expr='icontains')
    data_source = django_filters.CharFilter(lookup_expr='icontains')
    agency = django_filters.CharFilter(lookup_expr='iexact')
    sort = django_filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('goal', 'goal'),
            ('code', 'code'),
            ('stats_available', 'stats_available'),
        ))

    class Meta:
        model = Indicator
        fields = ['goal', 'code', 'stats_available']


class ComponentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    goal = django_filters.ModelChoiceFilter(name='indicator__goal',
                                            queryset=Goal.objects.all())
    sort = django_filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('indicator', 'indicator'),
            ('code', 'code'),
            ('created', 'created'),
            ('last_modified', 'last_modified'),
        ))

    class Meta:
        model = Component
        fields = ['indicator', 'code']


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
