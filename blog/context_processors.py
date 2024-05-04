from .models import BlogPost

def latest_blog_posts(request):
    latest_posts = BlogPost.objects.order_by('-created_at')[:5]
    return {'latest_blog_posts': latest_posts}

def is_blog_page(request):
    print('bak buradasin ')
    context={'is_blog_page': request.path.startswith('/blogs/')}
    return  context