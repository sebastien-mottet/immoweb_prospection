"""insens URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers

from searches.views import SearchesViewSet
from properties.views import PropertiesViewSet
from prospection.views import ProspectionRulesViewSet, ProspectionLogsViewSet

router = routers.DefaultRouter()
router.register(r'searches', SearchesViewSet)
router.register(r'properties', PropertiesViewSet)
router.register(r'prospection_rules', ProspectionRulesViewSet)
router.register(r'prospection_logs', ProspectionLogsViewSet)

urlpatterns = [
    path('api-v1/', include(router.urls)),
    path('admin/', admin.site.urls),
]
