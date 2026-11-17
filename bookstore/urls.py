from django.contrib import admin
from django.conf import settings
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/', include('api.urls')),
]

