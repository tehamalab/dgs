from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import HStoreField
from mptt.admin import DraggableMPTTAdmin
from import_export.admin import ImportExportModelAdmin
from django_postgres_utils.widgets import AdminHStoreWidget
from .models import (Plan, Goal, Theme, SectorType, Sector, Target, Indicator,
                     Component, Progress, Area, AreaType)
from .import_export import (AreaResource, GoalResource, ThemeResource,
                            SectorTypeResource, SectorResource, TargetResource,
                            IndicatorResource)


class HiddenExtrasMixin:

    def get_fieldsets(self, request, obj=None):
        print('called')
        if self.fieldsets:
            return self.fieldsets
        fields = self.get_fields(request, obj)
        fields.remove('extras')
        return [
            (None, {
                'fields': fields
            }),
            (_('Additional Info'), {
                'fields': ('extras',),
                'classes': ('collapse',)

            })
        ]


class ProgressInline(admin.TabularInline):
    model = Progress
    exclude = ['slug', 'extras']
    raw_id_fields = ['area']


class ComponentInline(admin.TabularInline):
    model = Component.indicators.through
    raw_id_fields = ['component']


class AreaTypeAdmin(HiddenExtrasMixin, ImportExportModelAdmin):
    search_fields = ['code', 'name']
    formfield_overrides = {
        HStoreField: {'widget': AdminHStoreWidget}
    }


class AreaAdmin(HiddenExtrasMixin, DraggableMPTTAdmin, ImportExportModelAdmin):
    resource_class = AreaResource
    search_fields = ['code', 'name']
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ['type']
    formfield_overrides = {
        HStoreField: {'widget': AdminHStoreWidget}
    }


class PlanAdmin(HiddenExtrasMixin, ImportExportModelAdmin):
    search_fields = ['^code', 'name']
    list_display = ['code', 'name', 'caption']
    list_display_links = ['code', 'name']
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}
    formfield_overrides = {
        HStoreField: {'widget': AdminHStoreWidget}
    }


class GoalAdmin(HiddenExtrasMixin, ImportExportModelAdmin):
    resource_class = GoalResource
    ordering = ['id']
    search_fields = ['^code', 'name', 'caption', 'plan__code',
                     'plan__name']
    list_display = ['plan_code', 'code', 'name', 'caption']
    list_display_links = ['code', 'name']
    list_filter = ['plan']
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}
    formfield_overrides = {
        HStoreField: {'widget': AdminHStoreWidget}
    }


class ThemeAdmin(HiddenExtrasMixin, ImportExportModelAdmin):
    resource_class = ThemeResource
    ordering = ['id']
    search_fields = ['^code', 'name', 'caption', 'plan__code',
                     'plan__name']
    list_display = ['plan_code', 'code', 'name', 'caption']
    list_display_links = ['code', 'name']
    list_filter = ['plan']
    save_on_top = True
    prepopulated_fields = {"slug": ("name",)}
    formfield_overrides = {
        HStoreField: {'widget': AdminHStoreWidget}
    }


class SectorTypeAdmin(HiddenExtrasMixin, ImportExportModelAdmin):
    resource_class = SectorTypeResource
    ordering = ['id']
    search_fields = ['^code', 'name']
    list_display = ['code', 'name', 'description']
    list_display_links = ['code', 'name']
    save_on_top = True
    formfield_overrides = {
        HStoreField: {'widget': AdminHStoreWidget}
    }


class SectorAdmin(HiddenExtrasMixin, DraggableMPTTAdmin, ImportExportModelAdmin):
    resource_class = SectorResource
    search_fields = ['^code', 'name', 'description']
    save_on_top = True
    filter_horizontal = ['themes']
    formfield_overrides = {
        HStoreField: {'widget': AdminHStoreWidget}
    }


class TargetAdmin(HiddenExtrasMixin, ImportExportModelAdmin):
    resource_class = TargetResource
    ordering = ['id']
    search_fields = ['^code', 'name', 'description']
    list_display = ['plan_code', 'code', 'name']
    list_display_links = ['code', 'name']
    list_filter = ['goal__plan', 'goal']
    save_on_top = True
    formfield_overrides = {
        HStoreField: {'widget': AdminHStoreWidget}
    }


class IndicatorAdmin(HiddenExtrasMixin, ImportExportModelAdmin):
    resource_class = IndicatorResource
    ordering = ['id']
    search_fields = ['^code', 'name', 'description', '=target__code']
    list_display = ['plan_code', 'code', 'name']
    list_display_links = ['code', 'name']
    list_filter = ['target__goal__plan', 'target__goal', 'theme', 'sector']
    save_on_top = True
    raw_id_fields = ['target']
    inlines = [ComponentInline]
    formfield_overrides = {
        HStoreField: {'widget': AdminHStoreWidget}
    }


class ComponentAdmin(HiddenExtrasMixin, ImportExportModelAdmin):
    ordering = ['id']
    search_fields = ['^code', 'name', 'description', '^indicators__code']
    list_display = ['code', 'name']
    list_display_links = ['code', 'name']
    list_filter = ['indicators__target__goal__plan',
                   'indicators__target__goal', 'stats_available', 'agency',
                   'data_source']
    prepopulated_fields = {"slug": ("name",)}
    save_on_top = True
    filter_horizontal = ['indicators']
    inlines = [ProgressInline]
    formfield_overrides = {
        HStoreField: {'widget': AdminHStoreWidget}
    }


class ProgressAdmin(HiddenExtrasMixin, ImportExportModelAdmin):
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
    save_on_top = True
    raw_id_fields = ['component']
    formfield_overrides = {
        HStoreField: {'widget': AdminHStoreWidget}
    }


admin.site.register(AreaType, AreaTypeAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(SectorType, SectorTypeAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Target, TargetAdmin)
admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Progress, ProgressAdmin)
