"""project_monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from django.urls import path
from databases.views import DatabaseViewSet, DBItemViewSet
from middleware.views import MiddlewareViewSet, MiddlewareItemViewSet
from server_monitor.views import ServerMonitorViewSet
from alarm.views import AlarmSeverityViewSet, AlarmStrategyViewSet, AlarmRuleViewSet, AlarmDetailViewSet
from network_monitor.views import NetworkMonitorViewSet, SeriesViewSet
from asset_relation.views import DeviceViewSet, BusinessViewSet, TagViewSet, StaffViewSet
from storage.views import StorageItemViewSet
from analysis.views import ServerAnalysisViewSet


router = DefaultRouter()
router.register(r'monitor/api/databases/*', DatabaseViewSet)
router.register(r'monitor/api/dbitem/*', DBItemViewSet)
router.register(r'monitor/api/middleware/*', MiddlewareViewSet)
router.register(r'monitor/api/middleware_item', MiddlewareItemViewSet)
router.register(r'monitor/api/server_monitor/*', ServerMonitorViewSet)
router.register(r'monitor/api/alarm_severity', AlarmSeverityViewSet)
router.register(r'monitor/api/alarm_strategy', AlarmStrategyViewSet)
router.register(r'monitor/api/alarm_rule', AlarmRuleViewSet)
router.register(r'monitor/api/alarm_detail/*', AlarmDetailViewSet)
router.register(r'monitor/api/network_monitor/*', NetworkMonitorViewSet)
router.register(r'monitor/api/series', SeriesViewSet)
router.register(r'monitor/api/device', DeviceViewSet)
router.register(r'monitor/api/business', BusinessViewSet)
router.register(r'monitor/api/tag', TagViewSet)
router.register(r'monitor/api/staff', StaffViewSet)
router.register(r'monitor/api/storageitem/*', StorageItemViewSet)
router.register(r'monitor/api/analysis/*', ServerAnalysisViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),

    # path('auth/', AuthView.as_view()),
]
