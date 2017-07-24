from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer
from ..search_indexes import (PlanIndex, GoalIndex, TargetIndex,
                              IndicatorIndex, ComponentIndex)


class SearchResultSerializer(HaystackSerializer):
    id = serializers.IntegerField(source='pk')
    api_url = serializers.SerializerMethodField()

    class Meta:
        index_classes = [PlanIndex, GoalIndex, TargetIndex,
                         IndicatorIndex, ComponentIndex]
        fields = ['code', 'name', 'description', 'slug',
                  'image', 'image_small', 'image_medium', 'image_large',
                  'plan', 'plan_code', 'plan_id', 'plan_name',
                  'goal', 'goal_code', 'goal_id', 'goal_name',
                  'target', 'target_code', 'target_id', 'target_name',
                  'indicators', 'indicators_names', 'indicators_codes',
                  'targets_ids', 'targets_codes', 'targets_names',
                  'goals_ids', 'goals_codes', 'goals_names',
                  'plans_ids', 'plans_codes', 'plans_names',
                  'progress_count', 'agency', 'data_source',
                  'stats_available', 'object_type', 'created',
                  'last_modified', 'content']

    def get_api_url(self, obj):
        return self.context.get('request')\
            .build_absolute_uri(obj.api_url)
