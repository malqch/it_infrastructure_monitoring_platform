"""project_pxeserver URL Configuration

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
# from django.contrib import admin
from django.urls import path
from job_install.views import BindMacView, CallPmSnIpView, RemoveMacView, \
    CheckPingView, ConfigIpView
from job_check.views import CallMacView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('pxeserver/api/addsystem/', BindMacView.as_view()),
    path('pxeserver/api/callnics/', CallMacView.as_view()),
    path('pxeserver/api/callpm_snip/', CallPmSnIpView.as_view()),
    path('pxeserver/api/removemac/', RemoveMacView.as_view()),
    path('pxeserver/api/checkping/', CheckPingView.as_view()),
    path('pxeserver/api/configip/', ConfigIpView.as_view())
]
