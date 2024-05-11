from .models import BlogPost, CustomUser, Industry

def latest_blog_posts(request):
    latest_posts = BlogPost.objects.order_by('-created_at')[:5]
    return {'latest_blog_posts': latest_posts}

def latest_industry(request):

    superadmin = CustomUser.objects.filter(is_superuser=True).last()

    # Süper yöneticiye ait son üç endüstriyi alıyoruz
    latest_industries = Industry.objects.filter(user=superadmin).order_by('-id')[:5]
    context={
            'is_industry_page': request.path.startswith('/industries/'),
             'latest_industry':latest_industries
             }
    return context

def is_blog_page(request):
    context={'is_blog_page': request.path.startswith('/blogs/')}
    return  context