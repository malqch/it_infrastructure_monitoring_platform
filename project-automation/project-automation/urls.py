"""project_automation URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from patrol.views import PatrolViewSet
from script.views import ScriptViewSet, ScriptLogViewSet, ScriptTimedTaskViewSet
from install.views import PxeServerViewSet, PxeServerOsViewSet, JobCheckViewSet, JobInstallViewSet, PmPortViewSet
from huaweiyun.views import HuaweiyunViewSet
from script import views as v
from storage.views import StorageViewSet
from host.views import HostViewSet

router = DefaultRouter()
router.register(r'automation/api/script', ScriptViewSet)
router.register(r'automation/api/script_log', ScriptLogViewSet)
router.register(r'automation/api/script_timed_task', ScriptTimedTaskViewSet)
router.register(r'automation/api/pxe_server', PxeServerViewSet)
router.register(r'automation/api/pxe_server_os', PxeServerOsViewSet)
router.register(r'automation/api/job_check', JobCheckViewSet)
router.register(r'automation/api/job_install', JobInstallViewSet)
router.register(r'automation/api/pm_port', PmPortViewSet)
router.register(r'automation/api/huawei', HuaweiyunViewSet)
router.register(r'automation/api/storage', StorageViewSet, basename='storage')
router.register(r'automation/api/host/*', HostViewSet, basename='host')
router.register(r'automation/api/patrol/*', PatrolViewSet, basename='patrol')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^ws/executing_script', v.executing_script),
    url(r'^ws/immediate_exec_script', v.immediate_exec_script),
    # path('admin/', admin.site.urls),
]
