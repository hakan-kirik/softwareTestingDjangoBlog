def main_menu():
    print("1- Ana Sayfa ve Navigasyon Testleri Çalıştır")
    print("2- Kullanıcı Blog Testleri Çalıştır")
    print("3- Endüstri Sayfaları Testleri Çalıştır")
    print("4- Popup ve İmaj Kontrol Testleri Çalıştır")
    print("5- Popup Login Testlerini Çalıştır")
    print("6- Admin Blog Testlerini Çalıştır (kapsamlı test)")
    choice = input("Lütfen test numarasını giriniz: ")
    if choice == '1':
        from .testhomepage import run_tests as run_home_tests
        run_home_tests()
    elif choice == '2':
        from .userBlogTest import run_blog_tests
        username = 'test'  #super user olmayan kullanici 
        password = 'hako123'
        run_blog_tests(username, password)
    elif choice == '3':
        from .industryPage import run_tests as run_industry_test
        run_industry_test()
    elif choice == '4':
        # Popup ve İmaj Kontrol Testlerini burada çağır
        pass
    elif choice == '5':
        username = input("Kullanıcı adını giriniz: ")
        password = input("Şifreyi giriniz: ")
        from .modalLoginTest import run_tests as run_login_tests
        run_login_tests(username, password)
    elif choice == '6':
        username = 'hako' #input("Kullanıcı adını giriniz: ")
        password = 'hako123' #input("Şifreyi giriniz: ")
        from .adminBlogTest import run_tests as run_admin_blog_tests
        run_admin_blog_tests(username, password)
    else:
        print("Geçersiz seçim.")

if __name__ == "__main__":
    main_menu()


