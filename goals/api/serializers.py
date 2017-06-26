from rest_framework import serializers
from ..models import (Area, Plan, Goal, Target, Indicator, Component,
                      Progress)


class AreaSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Area
        exclude = ['tree_id']


class PlanSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Plan
        fields = '__all__'


class GoalSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Goal
        exclude = []


class TargetSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Target
        exclude = []


class IndicatorSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Indicator
        exclude = []


class ProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Progress
        exclude = []


class ComponentSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Component
        exclude = []
