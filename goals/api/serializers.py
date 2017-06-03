from rest_framework import serializers
from ..models import Area, Goal, Indicator, Component, Progress


class AreaSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Area
        exclude = []


class GoalSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Goal
        exclude = []


class IndicatorSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Indicator
        exclude = []


class ComponentSerializer(serializers.ModelSerializer):
    image_small = serializers.ImageField(read_only=True)
    image_medium = serializers.ImageField(read_only=True)
    image_large = serializers.ImageField(read_only=True)

    class Meta:
        model = Component
        exclude = []


class ProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Progress
        exclude = []
