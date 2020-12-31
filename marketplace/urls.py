# Django
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# App mkt
from apps.mkt.views import vHome

urlpatterns = [
    path('', include('apps.mkt.urls', namespace = 'mkt')),
    path('user/', include('apps.users.urls', namespace = 'user')),
    path('admin/', include('apps.admin.urls', namespace = 'admin'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)