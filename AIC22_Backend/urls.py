"""AIC22_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static

from AIC22_Backend.settings import STATIC_URL, MEDIA_URL, STATIC_ROOT, MEDIA_ROOT, IS_PRODUCTION, SENTRY_ENABLED
from routers import CustomRouter
from website.urls import website_router
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

AIC_v1_router = CustomRouter()
AIC_v1_router.extend(website_router)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/v1/', include(AIC_v1_router.urls)),
                  path('api/v1/account/', include('account.urls')),
                  path('api/v1/challenge/', include('challenge.urls')),
                  path('api-doc/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('api-auth/', include('rest_framework.urls')),
                  path('summernote/', include('django_summernote.urls')),
                  path('api/v1/team/', include('team.urls')),
                  path('api/v1/communication/', include('communication.urls')),
                  path(
                      'api-doc/schema/swagger-ui/',
                      SpectacularSwaggerView.as_view(url_name='schema'),
                      name='swagger-ui',
                  ),
                  path(
                      'api-doc/schema/redoc/',
                      SpectacularRedocView.as_view(url_name='schema'),
                      name='redoc',
                  ),
              ] + static(STATIC_URL, document_root=STATIC_ROOT) + static(MEDIA_URL, document_root=MEDIA_ROOT)
