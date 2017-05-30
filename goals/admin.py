from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Goal, Indicator, Component, Progress


class ProgressInline(admin.TabularInline):
    model = Progress


class GoalAdmin(ImportExportModelAdmin):
    list_display = ['code', 'name', 'description']
    list_display_links = ['code', 'name']
    prepopulated_fields = {"slug": ("name",)}
    ordering = ['id']


class IndicatorAdmin(ImportExportModelAdmin):
    list_display = ['code', 'description']
    list_display_links = ['code', 'description']
    list_filter = ['goal']
    search_fields = ['code', 'description']
    ordering = ['id']


class ComponentAdmin(ImportExportModelAdmin):
    list_display = ['code', 'name']
    list_display_links = ['code', 'name']
    list_filter = ['indicator__goal']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['code', 'name']
    ordering = ['id']
    inlines = [ProgressInline]


class ProgressAdmin(ImportExportModelAdmin):
    list_display = ['component_code', 'component_name', 'year', 'value',
                    'value_unit']
    list_display_links = ['component_name', 'year', 'value']
    list_filter = ['year', 'component__indicator']
    search_fields = ['component__indicator__code',
                     'component__indicator__description']
    ordering = ['id']
    list_select_related = ['component']


admin.site.register(Goal, GoalAdmin)
admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Progress, ProgressAdmin)
