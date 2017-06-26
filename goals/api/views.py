from rest_framework import viewsets
from .serializers import (AreaSerializer, PlanSerializer,
                          GoalSerializer, TargetSerializer,
                          IndicatorSerializer, ComponentSerializer,
                          ProgressSerializer)
from ..models import (Area, Plan, Goal, Target, Indicator, Component,
                      Progress)
from ..filters import (AreaFilter, PlanFilter, GoalFilter, TargetFilter,
                       IndicatorFilter, ComponentFilter, ProgressFilter)


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    filter_class = AreaFilter
    ordering_fields = ('id', 'code', 'name', 'type')
    ordering = ('name',)


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    filter_class = PlanFilter
    ordering_fields = ('id', 'code', 'name')
    ordering = ('id',)


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.prefetch_related('plan')
    serializer_class = GoalSerializer
    filter_class = GoalFilter
    ordering_fields = ('id', 'code', 'name')
    ordering = ('id',)


class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    filter_class = TargetFilter
    ordering_fields = ('id', 'code', 'goal')
    ordering = ('code',)


class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    filter_class = IndicatorFilter
    ordering_fields = ('id', 'code', 'stats_available')
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
