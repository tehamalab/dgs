from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer
from ..search_indexes import (PlanIndex, GoalIndex, ThemeIndex, SectorIndex,
                              TargetIndex, IndicatorIndex, ComponentIndex)


class SearchResultSerializer(HaystackSerializer):
    id = serializers.IntegerField(source='pk')
    api_url = serializers.SerializerMethodField()

    class Meta:
        index_classes = [PlanIndex, ThemeIndex, SectorIndex, GoalIndex,
                         TargetIndex, IndicatorIndex, ComponentIndex]
        fields = ['code', 'name', 'caption', 'description', 'slug',
                  'image', 'image_small', 'image_medium', 'image_large',
                  'plan', 'plan_code', 'plan_id', 'plan_name',
                  'plans_ids', 'plans_codes', 'plans_names',
                  'sector', 'sector_id', 'sector_code', 'sector_name',
                  'sectors_ids', 'sectors_codes', 'sectors_names',
                  'theme', 'theme_id', 'theme_code', 'theme_name',
                  'themes_ids', 'themes_names', 'themes_codes',
                  'goal', 'goal_code', 'goal_id', 'goal_name',
                  'goals_ids', 'goals_codes', 'goals_names',
                  'target', 'target_code', 'target_id', 'target_name',
                  'targets_ids', 'targets_codes', 'targets_names',
                  'indicators', 'indicators_names', 'indicators_codes',
                  'progress_count', 'agency', 'data_source',
                  'parent', 'parent_name', 'level',
                  'stats_available', 'object_type', 'created',
                  'last_modified', 'content']

    def get_api_url(self, obj):
        return self.context.get('request')\
            .build_absolute_uri(obj.api_url)
