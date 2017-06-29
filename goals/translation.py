from modeltranslation.translator import register, TranslationOptions
from .models import Plan, Goal, Target, Indicator, Component


@register(Plan)
class PlanTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'image')


@register(Goal)
class GoalTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'image')


@register(Target)
class TargetTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'image')


@register(Indicator)
class IndicatorTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'image')


@register(Component)
class ComponentTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'image', 'agency', 'data_source')
