from django.contrib import admin
from django.conf import settings
from django.urls import path, include
import debug_toolbar
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/', include('api.urls')),
    path('api/auth/', obtain_auth_token, name='api_token_auth'),
]

