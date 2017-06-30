from django.apps import apps
from haystack.inputs import Raw
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_haystack.viewsets import HaystackViewSet
from haystack_elasticsearch5.query import SearchQuerySet
from .serializers import SearchResultSerializer
from ..filters import SimpleFilterBackend


Plan = apps.get_registered_model('goals', 'Plan')
Goal = apps.get_registered_model('goals', 'Goal')
Target = apps.get_registered_model('goals', 'Target')
Indicator = apps.get_registered_model('goals', 'Indicator')
Component = apps.get_registered_model('goals', 'Component')


class SearchViewSet(HaystackViewSet):

    index_models = [Plan, Goal, Target, Indicator, Component]
    serializer_class = SearchResultSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SimpleFilterBackend]
    filter_fields = [
        'code', 'name', 'description', 'slug', 'plan', 'plan_code',
        'plan_id', 'plan_name', 'goal', 'goal_code', 'goal_id',
        'goal_name', 'target', 'target_code', 'target_id',
        'target_name', 'indicators', 'indicators_names',
        'indicators_codes', 'targets_ids', 'targets_codes',
        'targets_names', 'goals_ids', 'goals_codes', 'goals_names',
        'plans_ids', 'plans_codes', 'plans_names', 'agency',
        'data_source', 'stats_available', 'object_type', 'created',
        'last_modified', 'content']
    boost_fields = {
        'code': 1.5,
        'name': 3,
        'description': 1,
        'plan_name': 1,
        'goal_name': 1,
        'target_name': 1,
        'plan_names': 1,
        'goals_names': 1,
        'targets_names': 1,
        'indicators_names': 1,
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
