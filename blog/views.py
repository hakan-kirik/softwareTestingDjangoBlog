from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.db.models import Count

from blog.models import BlogPost, Category,Comment

# Create your views here.

def home(request):
    return render(request,'index.html')

def blogs(request):
    blog_posts = BlogPost.objects.all()
    paginator = Paginator(blog_posts, 10)  # Sayfa başına 10 gönderi göster
    page = request.GET.get('page')
    try:
        blog_posts = paginator.page(page)
    except PageNotAnInteger:
        blog_posts = paginator.page(1)
    except EmptyPage:
        blog_posts = paginator.page(paginator.num_pages)
    return render(request, 'blogs.html', {'blog_posts': blog_posts})

def blog(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
 
    previous_post = BlogPost.objects.filter(id__lt=pk).order_by('-id').first()
    next_post = BlogPost.objects.filter(id__gt=pk).order_by('id').first()
    recent_posts = BlogPost.objects.all()[:3]  # Son 3 blog gönderisini alır
    categories = Category.objects.annotate(post_count=Count('blogpost')).order_by('name')
 
    context = {
        'blog_post': blog_post,
        'previous_post': previous_post,
        'next_post': next_post,
        'page_title': blog_post.title,  # Sayfa başlığı olarak blog gönderisinin başlığını kullanabiliriz
        'breadcrumb': [('Home', reverse('home')), ('Blog', reverse('blogs'))],  # Breadcrumb listesi
        'recent_posts': recent_posts,
        'categories': categories,
    }
    return render(request, 'blog.html', context)
def add_comment(request, blog_id):
    blog_post = get_object_or_404(BlogPost, pk=blog_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(blog_post=blog_post, author=request.user, content=content)
        return redirect('blog-detail', pk=blog_id)
    return redirect('blog-detail', pk=blog_id)

# def comment_create(request, blog_id):
#     # İlgili blog gönderisi alınıyor
#     blog_post = get_object_or_404(BlogPost, id=blog_id)
    
#     # POST isteği kontrol ediliyor
#     if request.method == 'POST':
#         # İstekten gelen veriler form'a dolduruluyor
#         form = CommentForm(request.POST)
#         # Formun geçerli olup olmadığı kontrol ediliyor
#         if form.is_valid():
#             # Yorum nesnesi oluşturuluyor ancak henüz veritabanına kaydedilmiyor
#             comment = form.save(commit=False)
#             # Yorumun blog gönderisine bağlanması
#             comment.blog_post = blog_post
#             # Yorumun yazarının atanması
#             comment.author = request.user
#             # Yorumun veritabanına kaydedilmesi
#             comment.save()
#             # Yorum başarıyla oluşturulduktan sonra blog detay sayfasına yönlendirme
#             return redirect('blog-detail', blog_id=blog_id)
#     else:
#         # GET isteği için boş bir form oluşturuluyor
#         form = CommentForm()
#     # Form şablonu ve ilgili bilgilerle birlikte render ediliyor
#     return render(request, 'comment_create.html', {'form': form, 'blog_post': blog_post})
