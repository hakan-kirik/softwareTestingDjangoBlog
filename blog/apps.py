from django.apps import AppConfig



class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    def ready(self):
            # Uygulama başladığında bu kod çalışacak
            try:
                from django.contrib.auth.models import Group, Permission
                from django.contrib.contenttypes.models import ContentType
                from blog.models import BlogPost, Industry
                # Grup oluştur, varsa hata almayalım
                group, created = Group.objects.get_or_create(name='Blogger')
                if created:

                    # BlogPost modeli üzerinde hangi izinlerin verileceğini belirle
                    blogpost_content_type = ContentType.objects.get_for_model(BlogPost)
                    blogpost_permissions = Permission.objects.filter(content_type=blogpost_content_type)
                
        
                    # Industry modeli üzerinde hangi izinlerin verileceğini belirle
                    industry_content_type = ContentType.objects.get_for_model(Industry)
                    industry_permissions = Permission.objects.filter(content_type=industry_content_type)
                    permissions = blogpost_permissions.union(industry_permissions)
                    group.permissions.set(permissions)
                    # Kullanıcılara izinleri atadıktan sonra grupları kaydet
                    group.save()
                    print("Blogger oluşturuldu.")
                else:
                    print("Blogger zaten mevcut.")
            except Exception as e:
                print("Grup oluşturulurken bir hata oluştu:", e)



