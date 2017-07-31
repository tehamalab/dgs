from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from import_export.admin import ImportExportModelAdmin
from .models import (Plan, Goal, Target, Indicator, Component, Progress,
                     Area, AreaType)
from .import_export import (AreaResource, GoalResource, TargetResource,
                            IndicatorResource)


class ProgressInline(admin.TabularInline):
    model = Progress
    exclude = ['slug', 'extras']
    raw_id_fields = ['area']


class ComponentInline(admin.TabularInline):
    model = Component.indicators.through
    raw_id_fields = ['component']


class AreaTypeAdmin(ImportExportModelAdmin):
    search_fields = ['code', 'name']


class AreaAdmin(DraggableMPTTAdmin, ImportExportModelAdmin):
    resource_class = AreaResource
    search_fields = ['code', 'name']
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ['type']


class PlanAdmin(ImportExportModelAdmin):
    search_fields = ['^code', 'name']
    list_display = ['code', 'name', 'description']
    list_display_links = ['code', 'name']
    prepopulated_fields = {"slug": ("name",)}


class GoalAdmin(ImportExportModelAdmin):
    resource_class = GoalResource
    ordering = ['id']
    search_fields = ['^code', 'name', 'description', 'plan__code',
                     'plan__name']
    list_display = ['plan_code', 'code', 'name', 'description']
    list_display_links = ['code', 'name']
    list_filter = ['plan']
    prepopulated_fields = {"slug": ("name",)}


class TargetAdmin(ImportExportModelAdmin):
    resource_class = TargetResource
    ordering = ['id']
    search_fields = ['^code', 'name', 'description']
    list_display = ['plan_code', 'code', 'name']
    list_display_links = ['code', 'name']
    list_filter = ['goal__plan', 'goal']


class IndicatorAdmin(ImportExportModelAdmin):
    resource_class = IndicatorResource
    ordering = ['id']
    search_fields = ['^code', 'name', 'description', '=target__code']
    list_display = ['plan_code', 'code', 'name']
    list_display_links = ['code', 'name']
    list_filter = ['target__goal__plan', 'target__goal']
    raw_id_fields = ['target']
    inlines = [ComponentInline]


class ComponentAdmin(ImportExportModelAdmin):
    ordering = ['id']
    search_fields = ['^code', 'name', 'description', '^indicators__code']
    list_display = ['code', 'name']
    list_display_links = ['code', 'name']
    list_filter = ['indicators__target__goal__plan',
                   'indicators__target__goal', 'stats_available', 'agency',
                   'data_source']
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ['indicators']
    inlines = [ProgressInline]


class ProgressAdmin(ImportExportModelAdmin):
    ordering = ['id']
    search_fields = ['component__name', '^component__code',
                 '^component__indicators__code',
                 'component__indicators__name']
    list_display = ['component_code', 'component_name', 'groups', 'year',
                    'value', 'value_unit']
    list_display_links = ['component_name', 'year', 'value']
    list_filter = [
        'year',
        'fiscal_year', 
        'component__indicators__target__goal__plan',
        'component__indicators__target__goal'
    ]
    list_select_related = ['component']
    raw_id_fields = ['component']


admin.site.register(AreaType, AreaTypeAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Target, TargetAdmin)
admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Progress, ProgressAdmin)

