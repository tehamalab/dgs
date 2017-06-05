from rest_framework import viewsets
from .serializers import (AreaSerializer, GoalSerializer,
                          IndicatorSerializer, ComponentSerializer,
                          ProgressSerializer)
from ..models import Area, Goal, Indicator, Component, Progress
from ..filters import (AreaFilter, GoalFilter, IndicatorFilter,
                       ComponentFilter, ProgressFilter)


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    filter_class = AreaFilter
    ordering_fields = ('id', 'code', 'name', 'type')
    ordering = ('name',)


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    filter_class = GoalFilter
    ordering_fields = ('id', 'code', 'name')
    ordering = ('id',)


class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    filter_class = IndicatorFilter
    ordering_fields = ('id', 'code', 'goal', 'stats_available')
    ordering = ('code',)


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.prefetch_related('progress')
    serializer_class = ComponentSerializer
    filter_class = ComponentFilter
    ordering_fields = ('id', 'code', 'indicator', 'created',
                       'last_modified')
    ordering = ('code',)


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    filter_class = ProgressFilter
    ordering_fields = ('id', 'year', 'value', 'area',
                       'last_modified', 'created')
    ordering = ('-year',)
