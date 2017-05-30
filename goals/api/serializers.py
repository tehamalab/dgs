from rest_framework import serializers
from ..models import Area, Goal, Indicator, Component, Progress


class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        exclude = []


class GoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        exclude = []


class IndicatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Indicator
        exclude = []


class ComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Component
        exclude = []


class ProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Progress
        exclude = []
