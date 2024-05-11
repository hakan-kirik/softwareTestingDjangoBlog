
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blog import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('blogs/blog/<int:pk>/',views.blog,name='blog-detail'),
    path('blog/<int:blog_id>/add_comment/', views.add_comment, name='add_comment'),
    path('comment/create/<int:blog_id>/', views.add_comment, name='comment-create'),
    path('blogs/', views.blogs,name='blogs'),
    path('industries/industry/<int:pk>',views.Industryw,name='industry'),
    path('industries/',views.Industries,name='industries'),
    path('comment-create/<int:pk>/', views.CommentCreateView.as_view(), name='comment-create'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('custom-login/', views.CustomLoginView.as_view(), name='login'),
    path('ajax-login/', views.ajax_login, name='ajax_login'),
    path('register/', views.register, name='register'),
    path('',views.home,name='home')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)