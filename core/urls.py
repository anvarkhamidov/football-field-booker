"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from field.views import FieldViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Football Field Booking API",
        default_version="v1",
        description="API documentation",
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)
router = DefaultRouter(trailing_slash=False)
router.register(r"fields", FieldViewSet, basename="field")

urlpatterns = [
    path(
        "docs",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("", include(router.urls)),
    path("", include("booking.urls")),
    path("user", include("user.urls")),
    path("admin", admin.site.urls),
]
