from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.db.models import Count
from django.views.generic import View
from blog.FormModels.CommentForm import CommentForm
from blog.FormModels.RegisterForm import RegisterForm
from blog.models import BlogPost, Category,Comment, CustomUser, Industry
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
# Create your views here.

def home(request):
    superadmin = CustomUser.objects.filter(is_superuser=True).last()

    # Süper yöneticiye ait son üç endüstriyi alıyoruz
    latest_industries = Industry.objects.filter(user=superadmin).order_by('-id')[:3]
    latest_posts = BlogPost.objects.all().order_by('-created_at')[:3]
    context={
        'industries': latest_industries,
        'latest_posts':latest_posts
    }
    return render(request,'index.html' ,context)

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
        'breadcrumb': [('Ana Sayfa', reverse('home')), ('Blog', reverse('blogs'))],  # Breadcrumb listesi
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


def Industries(request):
    industries_list = Industry.objects.all()
    paginator = Paginator(industries_list, 10)  # Sayfa başına 10 endüstri göstermek için bir Paginator oluşturun

    page_number = request.GET.get('page')
    try:
        industries = paginator.page(page_number)
    except PageNotAnInteger:
        # Eğer sayfa numarası bir tam sayı değilse, ilk sayfayı getir
        industries = paginator.page(1)
    except EmptyPage:
        # Eğer sayfa numarası geçerli değilse, son sayfayı getir
        industries = paginator.page(paginator.num_pages)

    return render(request, 'industries.html', {'industries_list': industries})

def Industryw(request,pk):
    latest_industries = Industry.objects.order_by('-created_at')[:5]
    industry = get_object_or_404(Industry, pk=pk)
    context={'latest_industries': latest_industries,
             'industry': industry
             }

    return render(request,'industry.html',context)

class CommentCreateView(LoginRequiredMixin, View):
    def get_login_url(self):
        # İstek objesine erişerek isteğin PK değerini alıyoruz
        pk = self.kwargs.get('pk')
        # dinamik olarak pk değerini içeren login_url oluşturuyoruz
        return reverse('blog-detail', kwargs={'pk': pk})
    
    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_post_id = pk
            comment.author = request.user
            comment.save()
            return redirect('blog-detail', pk=pk)
        else:
            # Form validation failed
            # Handle the error or display a message
            return redirect('blog-detail', pk=pk)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Kullanıcının oturum açmış olup olmadığını kontrol ediyoruz
        if self.request.user.is_authenticated:
            # Oturum açmışsa kullanıcının bilgilerini context'e ekliyoruz
            context['isnot_authenticated'] = False
        else:
            context['isnot_authenticated'] = True
        return context

    redirect_field_name = 'next'  # Kullanıcının geldiği URL'i hatırlamak için kullanılan isim



class CustomLoginView(View):
    def post(self, request):
        # Kullanıcı adı ve parola formdan alınıyor
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Kullanıcı doğrulanıyor
        user = authenticate(username=username, password=password)

        if user is not None:
            # Kullanıcı doğrulandıysa oturum açılıyor
            login(request, user)

            # Eğer 'next' parametresi varsa, oraya yönlendir
            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                # 'next' parametresi yoksa varsayılan olarak admin paneline yönlendir
                return HttpResponseRedirect(reverse('admin:index'))
        else:
            # Kullanıcı doğrulanamazsa, giriş sayfasına geri yönlendir
            return HttpResponseRedirect(reverse('login'))

def ajax_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'message': 'Invalid credentials'})

@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']  # Kullanıcı adını al
        password = form.cleaned_data['password1']
        # Yeni kullanıcı oluştur
        user = CustomUser.objects.create_user(email=email, username=username, password=password)
        # Oturumu aç
        user = authenticate(username=username, password=password)
        login(request, user)
        # Başarılı kayıt olduktan sonra JSON yanıtı döndür
        return JsonResponse({'status': 'success'})
    else:
        # Hatalı form durumunda hata mesajlarını JSON yanıtı olarak döndür
        errors = dict(form.errors.items())
        return JsonResponse({'status': 'error', 'errors': errors}, status=400)