from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from settings import settings

urlpatterns = [
    path('', include('tasks_manager.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
