from modeltranslation.translator import register, TranslationOptions
from .models import (AreaType, Area, Plan, Theme, SectorType, Sector, Goal,
                     Target, Indicator, Component)


@register(AreaType)
class AreaTypeTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Area)
class AreaTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'image')


@register(Plan)
class PlanTranslationOptions(TranslationOptions):
    fields = ('name', 'caption', 'description', 'image')


@register(Goal)
class GoalTranslationOptions(TranslationOptions):
    fields = ('name', 'caption', 'description', 'image')


@register(Theme)
class ThemeTranslationOptions(TranslationOptions):
    fields = ('name', 'caption', 'description', 'image')


@register(Sector)
class SectorTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'image')


@register(SectorType)
class SectorTypeTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Target)
class TargetTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'image')


@register(Indicator)
class IndicatorTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'image')


@register(Component)
class ComponentTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'image', 'agency', 'data_source')
