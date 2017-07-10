import json
from import_export import widgets, resources, fields
from .models import (Area, Goal, Target, Indicator)


class HStoreWidget(widgets.Widget):
    """
    Widget for converting HStore fields.
    """

    def clean(self, value, row=None, *args, **kwargs):
        if value is None or value == "":
            return None
        return json.loads(value)


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


class AreaResource(resources.ModelResource):
    parent = fields.Field(
        attribute='parent', widget=widgets.ForeignKeyWidget(Area))
    extras = fields.Field(attribute='extras', widget=HStoreWidget())

    class Meta:
        model = Area
