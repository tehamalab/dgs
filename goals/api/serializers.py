from django.forms.models import model_to_dict
from rest_framework import serializers
from ..models import (Area, AreaType, Plan, Theme, SectorType, Sector,
                      Goal, Target, Indicator, Component, Progress)


class ProgressSerializer(serializers.ModelSerializer):
    area_code = serializers.CharField(read_only=True)
    area_name = serializers.CharField(read_only=True)
    area_type_id = serializers.IntegerField(read_only=True,
                                            allow_null=True)
    area_type_name = serializers.CharField(read_only=True)
    area_type_code = serializers.CharField(read_only=True)
    value_unit = serializers.CharField(read_only=True)

    class Meta:
        model = Progress
        exclude = []


class AreaTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AreaType
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)
    type_code = serializers.CharField(read_only=True)
    type_name = serializers.CharField(read_only=True)

    class Meta:
        model = Area
        fields = '__all__'


class SectorTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SectorType
        fields = '__all__'


class SectorSerializer(serializers.ModelSerializer):
    api_url = serializers.SerializerMethodField()

    class Meta:
        model = Sector
        fields = '__all__'

    def get_api_url(self, obj):
        return self.context.get('request')\
            .build_absolute_uri(obj.api_url)


class PlanSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)
    api_url = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = '__all__'

    def get_api_url(self, obj):
        return self.context.get('request')\
            .build_absolute_uri(obj.api_url)


class ThemeSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)
    plan_id = serializers.IntegerField(read_only=True)
    plan_code = serializers.CharField(read_only=True)
    plan_name = serializers.CharField(read_only=True)
    api_url = serializers.SerializerMethodField()

    class Meta:
        model = Theme
        exclude = []

    def get_api_url(self, obj):
        return self.context.get('request')\
            .build_absolute_uri(obj.api_url)


class GoalSerializer(ThemeSerializer):

    class Meta:
        model = Goal
        exclude = []


class TargetSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)
    goal_code = serializers.CharField(read_only=True)
    goal_name = serializers.CharField(read_only=True)
    plan_id = serializers.IntegerField(read_only=True)
    plan_code = serializers.CharField(read_only=True)
    plan_name = serializers.CharField(read_only=True)
    api_url = serializers.SerializerMethodField()

    class Meta:
        model = Target
        exclude = []

    def get_api_url(self, obj):
        return self.context.get('request')\
            .build_absolute_uri(obj.api_url)


class IndicatorSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)
    target_code = serializers.CharField(read_only=True)
    target_name = serializers.CharField(read_only=True)
    goal_id = serializers.IntegerField(read_only=True)
    theme_code = serializers.CharField(read_only=True)
    theme_name = serializers.CharField(read_only=True)
    sector_code = serializers.CharField(read_only=True)
    sector_name = serializers.CharField(read_only=True)
    sector_type_code = serializers.CharField(read_only=True)
    sector_type_name = serializers.CharField(read_only=True)
    root_sector_id = serializers.IntegerField(read_only=True)
    root_sector_code = serializers.CharField(read_only=True)
    root_sector_name = serializers.CharField(read_only=True)
    goal_code = serializers.CharField(read_only=True)
    goal_name = serializers.CharField(read_only=True)
    plan_id = serializers.IntegerField(read_only=True)
    plan_code = serializers.CharField(read_only=True)
    plan_name = serializers.CharField(read_only=True)
    api_url = serializers.SerializerMethodField()
    progress_count = serializers.IntegerField(read_only=True)
    progress_preview = serializers.SerializerMethodField()

    class Meta:
        model = Indicator
        fields = '__all__'

    def get_progress_preview(self, obj):
        progress_preview = []
        if obj._prefetched_objects_cache['components']:
            for c in obj._prefetched_objects_cache['components']:
                for p in c.progress_preview:
                    progress_preview.append(model_to_dict(p))
        return progress_preview

    def get_api_url(self, obj):
        return self.context.get('request')\
            .build_absolute_uri(obj.api_url)


class ComponentSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)
    indicators_names = serializers.ListField(read_only=True)
    targets_ids = serializers.ListField(read_only=True)
    targets_codes = serializers.ListField(read_only=True)
    targets_names = serializers.ListField(read_only=True)
    goals_ids = serializers.ListField(read_only=True)
    goals_codes = serializers.CharField(read_only=True)
    goals_names = serializers.ListField(read_only=True)
    plans_ids = serializers.ListField(read_only=True)
    plans_codes = serializers.ListField(read_only=True)
    plans_names = serializers.ListField(read_only=True)
    progress_count = serializers.IntegerField(read_only=True)
    api_url = serializers.SerializerMethodField()

    class Meta:
        model = Component
        exclude = []

    def get_api_url(self, obj):
        return self.context.get('request')\
            .build_absolute_uri(obj.api_url)
