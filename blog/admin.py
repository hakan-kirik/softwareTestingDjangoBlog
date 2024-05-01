from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from blog.models import BlogPost, CustomUser
from django.utils.safestring import mark_safe
# Register your models here.

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'display_cover_image']
    search_fields = ['title']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'

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

admin.site.register(CustomUser, CustomUserAdmin)