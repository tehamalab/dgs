from django.apps import apps
from haystack.inputs import Raw
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_haystack.viewsets import HaystackViewSet
from haystack_es.query import SearchQuerySet
from .serializers import SearchResultSerializer
from .pagination import SearchPagination
from ..filters import SimpleFilterBackend


Plan = apps.get_registered_model('goals', 'Plan')
Goal = apps.get_registered_model('goals', 'Goal')
Target = apps.get_registered_model('goals', 'Target')
Indicator = apps.get_registered_model('goals', 'Indicator')
Component = apps.get_registered_model('goals', 'Component')


class SearchViewSet(HaystackViewSet):

    index_models = [Plan, Goal, Target, Indicator, Component]
    pagination_class = SearchPagination
    serializer_class = SearchResultSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SimpleFilterBackend]
    filter_fields = [
        'code', 'name', 'description', 'slug', 'caption',
        'plan', 'plan_code', 'plan_id', 'plan_name',
        'plans_ids', 'plans_codes', 'plans_names',
        'sector', 'sector_id', 'sector_code', 'sector_name',
        'sectors_ids', 'sectors_codes', 'sectors_names',
        'theme', 'theme_id', 'theme_code', 'theme_name',
        'themes_ids', 'themes_names', 'themes_codes',
        'goal', 'goal_code', 'goal_id', 'goal_name',
        'goals_ids', 'goals_codes', 'goals_names',
        'target', 'target_name', 'target_code', 'target_id',
        'targets_ids', 'targets_codes', 'targets_names',
        'indicators', 'indicators_names', 'indicators_codes',
        'agency', 'data_source', 'stats_available',
        'object_type', 'content', 'parent', 'parent_name', 'level',
        'created', 'last_modified',
        'progress_count__gt','progress_count__lt',
        'progress_count__gte','progress_count__lte']
    boost_fields = {
        'code': 1.5,
        'name': 3,
        'caption': 1.5,
        'description': 1,
        'plan_name': 1,
        'plan_code': 1,
        'plans_names': 1,
        'plans_codes': 1,
        'theme_name': 1,
        'themes_names': 1,
        'goal_name': 1,
        'goals_names': 1,
        'target_name': 1,
        'targets_names': 1,
        'indicators_names': 1,
        'sector_name': 1,
        'sectors_names': 1,
        'parent_name': 1,
        'data_source': 1,
        'agency': 1,
    }
  
    def get_queryset(self, index_models=[]):
        q = self.request.query_params.get('q', None)
        if q:
            return SearchQuerySet()\
                .filter(content=Raw(q))\
                .boost_fields(self.boost_fields)\
                .facet('object_type')
        return SearchQuerySet().facet('object_type')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['facets'] = queryset.facet_counts()
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
