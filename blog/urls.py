
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blog import views

urlpatterns = [
    path('blogs/blog/<int:pk>/',views.blog,name='blog-detail'),
    path('blog/<int:blog_id>/add_comment/', views.add_comment, name='add_comment'),
    path('comment/create/<int:blog_id>/', views.add_comment, name='comment-create'),
    path('blogs/', views.blogs,name='blogs'),
    path('',views.home,name='home')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)