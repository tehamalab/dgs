from import_export import resources
from .models import (Goal, Target, Indicator)


class GoalResource(resources.ModelResource):

    class Meta:
        model = Goal
        import_id_fields = ['code']


class TargetResource(resources.ModelResource):

    class Meta:
        model = Target
        import_id_fields = ['code']


class IndicatorResource(resources.ModelResource):

    class Meta:
        model = Indicator
        import_id_fields = ['code']
