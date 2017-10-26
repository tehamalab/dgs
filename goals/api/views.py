from django.utils import timezone
from django.template.defaultfilters import slugify
from django.db.models import Count, Prefetch
from rest_framework import viewsets
from .serializers import (AreaSerializer, AreaTypeSerializer,
                          PlanSerializer, ThemeSerializer, GoalSerializer,
                          SectorTypeSerializer, SectorSerializer,
                          TargetSerializer, IndicatorSerializer,
                          ComponentSerializer, ProgressSerializer)
from ..models import (AreaType, Area, Plan, Theme, SectorType, Sector, Goal,
                      Target, Indicator, Component, Progress)
from ..filters import (AreaFilter, PlanFilter, GoalFilter, ThemeFilter,
                       SectorFilter, TargetFilter, IndicatorFilter,
                       ComponentFilter, ProgressFilter)


class ModelViewSet(viewsets.ModelViewSet):

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(ModelViewSet, self).finalize_response(
            request, response, *args, **kwargs)
        filename = '%s-%s.csv' % (slugify(self.get_view_name()), timezone.now().isoformat())
        if response.accepted_renderer.format == 'csv':
            response['content-disposition'] = 'attachment; filename=%s' % filename
        return response


class AreaTypeViewSet(ModelViewSet):
    queryset = AreaType.objects.all()
    serializer_class = AreaTypeSerializer


class AreaViewSet(ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    filter_class = AreaFilter
    ordering_fields = ('id', 'code', 'name', 'type')


class PlanViewSet(ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    filter_class = PlanFilter
    ordering_fields = ('id', 'code', 'name')
    ordering = ('id',)


class ThemeViewSet(ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    filter_class = ThemeFilter
    ordering_fields = ('id', 'code', 'name')
    ordering = ('id',)


class SectorTypeViewSet(ModelViewSet):
    queryset = SectorType.objects.all()
    serializer_class = SectorTypeSerializer
    ordering_fields = ('id', 'code', 'name')
    ordering = ('id',)


class SectorViewSet(ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    filter_class = SectorFilter
    ordering_fields = ('id', 'code', 'name')


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
    serializer_class = IndicatorSerializer
    filter_class = IndicatorFilter
    ordering_fields = ('id', 'code', 'stats_available', 'progress_count')
    ordering = ('code',)

    def get_queryset(self):
        progq = Progress.objects\
            .order_by('component__indicators', '-year', 'area__level')\
            .distinct('component__indicators')
        return Indicator.objects\
            .annotate(progress_count=Count('components__progress'))\
            .prefetch_related(Prefetch('components__progress', to_attr='progress_preview', queryset=progq))


class ComponentViewSet(ModelViewSet):
    queryset = Component.objects.annotate(
        progress_count=Count('progress')).prefetch_related('indicators')
    serializer_class = ComponentSerializer
    filter_class = ComponentFilter
    ordering_fields = ('id', 'code', 'indicator', 'created',
                       'last_modified', 'progress_count')
    ordering = ('code',)


class ProgressViewSet(ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    filter_class = ProgressFilter
    ordering_fields = ('id', 'year', 'value', 'area',
                       'last_modified', 'created')
    ordering = ('-year',)
