from django.urls import path
from .views import upload_file, delete_file
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
