import json
from import_export import widgets, resources, fields
from .models import (Area, Goal, Target, Indicator)


class JSONWidget(widgets.Widget):
    """
    Widget for converting HStore fields.
    """

    def clean(self, value, row=None, *args, **kwargs):
        if value is None or value == "":
            return None
        return json.loads(value)


class GoalResource(resources.ModelResource):
    extras = fields.Field(attribute='extras', widget=JSONWidget())

    class Meta:
        model = Goal
        import_id_fields = ['code']


class TargetResource(resources.ModelResource):
    extras = fields.Field(attribute='extras', widget=JSONWidget())

    class Meta:
        model = Target
        import_id_fields = ['code']


class IndicatorResource(resources.ModelResource):
    extras = fields.Field(attribute='extras', widget=JSONWidget())

    class Meta:
        model = Indicator
        import_id_fields = ['code']


class AreaResource(resources.ModelResource):
    parent = fields.Field(
        attribute='parent', widget=widgets.ForeignKeyWidget(Area))
    extras = fields.Field(attribute='extras', widget=JSONWidget())

    class Meta:
        model = Area
