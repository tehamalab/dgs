from django.contrib import admin
from .models import Goal, Indicator, Component, Progress


admin.site.register(Goal)
admin.site.register(Indicator)
admin.site.register(Component)
admin.site.register(Progress)
