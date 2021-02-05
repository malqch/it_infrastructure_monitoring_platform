"""project-asset URL Configuration

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
from data_center.views import DatacenterViewSet, RoomViewSet, RackViewSet
from logic_resource.views import StaffViewSet, BusinessViewSet, ContractViewSet, VendorViewSet
from spare_parts.views import DiskViewSet, HbaViewSet, HcaViewSet, NicViewSet, SsdViewSet
from tag.views import TagViewSet
from device.views import DeviceViewSet, NetworkViewSet, VirtualServerViewSet,\
    SeriesViewSet, StorageViewSet
from nro_relation.views import DeviceViewSet2

router = DefaultRouter()
router.register(r'asset/api/datacenter', DatacenterViewSet)
router.register(r'asset/api/room', RoomViewSet)
router.register(r'asset/api/rack', RackViewSet)
router.register(r'asset/api/staff', StaffViewSet)
router.register(r'asset/api/business', BusinessViewSet)
router.register(r'asset/api/contract', ContractViewSet)
router.register(r'asset/api/vendor', VendorViewSet)
router.register(r'asset/api/tag', TagViewSet)

router.register(r'asset/api/disk', DiskViewSet)
router.register(r'asset/api/hba', HbaViewSet)
router.register(r'asset/api/hca', HcaViewSet)
router.register(r'asset/api/nic', NicViewSet)
router.register(r'asset/api/ssd', SsdViewSet)

router.register(r'asset/api/device', DeviceViewSet)
router.register(r'asset/api/network', NetworkViewSet)
router.register(r'asset/api/virtual_server', VirtualServerViewSet)
router.register(r'asset/api/storage', StorageViewSet)
router.register(r'asset/api/series', SeriesViewSet)
router.register(r'asset/api/nro/network/*', DeviceViewSet2)




urlpatterns = [
    url(r'^', include(router.urls)),
    # path('auth/', AuthView.as_view()),
]

