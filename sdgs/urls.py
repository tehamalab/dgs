"""sdgs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from goals.api import views as goals_views

router = routers.DefaultRouter()
router.register(r'areas', goals_views.AreaViewSet)
router.register(r'goals', goals_views.GoalViewSet)
router.register(r'indicators', goals_views.IndicatorViewSet)
router.register(r'components', goals_views.ComponentViewSet)
router.register(r'progress', goals_views.ProgressViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    
admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE', '')
admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER', '')
admin.site.index_title = getattr(settings, 'ADMIN_INDEX_TITLE', '')

