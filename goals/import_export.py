import json
from import_export import widgets, resources, fields
from .models import (Area, Goal, Theme, SectorType, Sector, Target, Indicator)


class JSONWidget(widgets.Widget):
    """
    Widget for converting HStore fields.
    """

    def clean(self, value, row=None, *args, **kwargs):
        if value is None or value == "":
            return None
        return json.loads(value)


class BaseResource(resources.ModelResource):
    extras = fields.Field(attribute='extras', widget=JSONWidget())


class ThemeResource(BaseResource):

    class Meta:
        model = Theme


class SectorTypeResource(BaseResource):

    class Meta:
        model = SectorType


class SectorResource(BaseResource):
    parent = fields.Field(
        attribute='parent', widget=widgets.ForeignKeyWidget(Sector))

    class Meta:
        model = Sector


class GoalResource(BaseResource):

    class Meta:
        model = Goal


class TargetResource(BaseResource):

    class Meta:
        model = Target


class IndicatorResource(BaseResource):

    class Meta:
        model = Indicator


class AreaResource(BaseResource):
    parent = fields.Field(
        attribute='parent', widget=widgets.ForeignKeyWidget(Area))

    class Meta:
        model = Area
