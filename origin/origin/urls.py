"""origin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from bonds.views import BondsViewSet
from rest_framework.routers import Route, SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token

router = SimpleRouter()
router.register(r"bonds", BondsViewSet, basename="bonds")

urlpatterns = router.urls + [
    path('admin/', admin.site.urls),
    path('auth_token/', obtain_auth_token),
]