
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blog import views

urlpatterns = [
    path('', views.test,name='test'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)