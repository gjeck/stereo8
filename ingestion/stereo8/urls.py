from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from rest_framework.authtoken import views as auth_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('core.api', namespace='api')),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/auth-token/', auth_views.obtain_auth_token),
    url(
        regex=r'^api/jwt-token/',
        view=TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    url(
        regex=r'^api/jwt-token/refresh/',
        view=TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
