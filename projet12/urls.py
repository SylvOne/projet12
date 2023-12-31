"""
URL configuration for projet12 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from epic_events.views import ClientViewSet, UserViewSet, ContractViewSet, CurrentUserView, EventViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'users', UserViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'events', EventViewSet)

urlpatterns = [
    # access to admin panel
    path('admin/', admin.site.urls),
    # connection user api
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # urls Clients, User, Contract, Event
    path('api/me/', CurrentUserView.as_view(), name='me'),
    path('api/', include(router.urls)),
]
