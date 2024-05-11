from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from blog.models import BlogPost, Category, CustomUser, Industry,  Tag,Comment
from django.utils.safestring import mark_safe
# Register your models here.

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

class BlogPostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ['title', 'author', 'created_at', 'display_cover_image','display_tags']
    search_fields = ['title', 'author__username', 'category__name', 'tags__name']
    list_filter = ['created_at', 'category__name', 'tags__name']
    date_hierarchy = 'created_at'
    required_fields = ['cover_image']
    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    display_tags.short_description = 'Tags'

    def display_cover_image(self, obj):
        if obj.cover_image:
            return mark_safe('<img src="{0}" width="100" height="100" />'.format(obj.cover_image.url))
        else:
            return "No Image"

    display_cover_image.short_description = 'Cover Image'
    def save_model(self, request, obj, form, change):
        if not obj.author_id:  # Eğer blog gönderisi oluşturulurken yazar belirtilmemişse
            obj.author = request.user  # Gönderiyi oluşturan kullanıcıyı yazar olarak atar
        obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:  # Süper kullanıcı değilse
            return qs.filter(author=request.user)  # Sadece kendi gönderilerini listeler
        return qs

    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            # Sadece süper kullanıcılar tüm gönderileri değiştirebilir
            return obj.author == request.user
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            # Sadece süper kullanıcılar tüm gönderileri silebilir
            return obj.author == request.user
        return super().has_delete_permission(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            if request.user.is_superuser:
                kwargs["queryset"] = CustomUser.objects.all()
            else:
                kwargs["queryset"] = CustomUser.objects.filter(username=request.user.username)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_form(self, request, obj=None, **kwargs):
        # Alanların "required" niteliğini ayarlar
        form = super().get_form(request, obj, **kwargs)
        for field_name in self.required_fields:
            form.base_fields[field_name].required = True
        return form

admin.site.register(BlogPost, BlogPostAdmin)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Diğer özel ayarlamaları yapabilirsiniz
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_blogger', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_blogger'),
        }),
    )


    def has_add_permission(self, request):
        # Sadece süper kullanıcılara ekleme izni ver
        return request.user.is_superuser
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'blog_post', 'created_at']
    search_fields = ['author__username', 'blog_post__title']
    list_filter = ['created_at']


class IndustryAdmin(admin.ModelAdmin):

    list_display = ['name', 'user']
    search_fields = ['name']
    required_fields = ['image']
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            if request.user.is_superuser:
                kwargs["queryset"] = CustomUser.objects.all()
            else:
                kwargs["queryset"] = CustomUser.objects.filter(username=request.user.username)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['user']
        return []
    
    def get_form(self, request, obj=None, **kwargs):
        # Alanların "required" niteliğini ayarlar
        form = super().get_form(request, obj, **kwargs)
        for field_name in self.required_fields:
            form.base_fields[field_name].required = True
        return form



admin.site.register(Industry, IndustryAdmin)


admin.site.register(Comment, CommentAdmin)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Tag)