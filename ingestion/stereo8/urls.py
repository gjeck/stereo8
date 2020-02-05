from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(('core.api', 'core'), namespace='api')),
    url(r'^api/auth/', include(('users.urls', 'users'), namespace='auth')),
]
