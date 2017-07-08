from django.utils import timezone
from django.template.defaultfilters import slugify
from rest_framework import viewsets
from .serializers import (AreaSerializer, AreaTypeSerializer,
                          PlanSerializer, GoalSerializer,
                          TargetSerializer, IndicatorSerializer,
                          ComponentSerializer, ProgressSerializer,
                          GroupSerializer)
from ..models import (AreaType, Area, Group, Plan, Goal, Target,
                      Indicator, Component, Progress)
from ..filters import (AreaFilter, PlanFilter, GoalFilter, TargetFilter,
                       IndicatorFilter, ComponentFilter, ProgressFilter)


class ModelViewSet(viewsets.ModelViewSet):

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(ModelViewSet, self).finalize_response(
            request, response, *args, **kwargs)
        filename = '%s-%s.csv' \
            %(slugify(self.get_view_name()), timezone.now().isoformat())
        if response.accepted_renderer.format == 'csv':
            response['content-disposition'] = 'attachment; filename=%s'\
                %filename
        return response


class AreaTypeViewSet(ModelViewSet):
    queryset = AreaType.objects.all()
    serializer_class = AreaTypeSerializer


class AreaViewSet(ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    filter_class = AreaFilter
    ordering_fields = ('id', 'code', 'name', 'type')
    ordering = ('name',)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PlanViewSet(ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    filter_class = PlanFilter
    ordering_fields = ('id', 'code', 'name')
    ordering = ('id',)


class GoalViewSet(ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    filter_class = GoalFilter
    ordering_fields = ('id', 'code', 'name')
    ordering = ('id',)


class TargetViewSet(ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    filter_class = TargetFilter
    ordering_fields = ('id', 'code', 'goal')
    ordering = ('code',)


class IndicatorViewSet(ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    filter_class = IndicatorFilter
    ordering_fields = ('id', 'code', 'stats_available')
    ordering = ('code',)


class ComponentViewSet(ModelViewSet):
    queryset = Component.objects.prefetch_related('indicators')
    serializer_class = ComponentSerializer
    filter_class = ComponentFilter
    ordering_fields = ('id', 'code', 'indicator', 'created',
                       'last_modified')
    ordering = ('code',)


class ProgressViewSet(ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    filter_class = ProgressFilter
    ordering_fields = ('id', 'year', 'value', 'area',
                       'last_modified', 'created')
    ordering = ('-year',)
