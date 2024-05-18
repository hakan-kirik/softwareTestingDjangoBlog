def run_selected_tests(choices):
    valid_choices = {'1', '2', '3', '4', '5', '6', '0'}
    
    for choice in choices:
        if choice not in valid_choices:

            print(f"\033[91m\nGeçersiz seçim: {choice}. Lütfen geçerli test numaralarını girin.\n\033[0m")
            return  # Geçersiz bir seçim varsa işleme devam etmiyoruz.
        
    for choice in choices:
        if choice == '1':
            from .testhomepage import run_tests as run_home_tests
            run_home_tests()
        elif choice == '2':
            from .userBlogTest import run_blog_tests
            username = 'test'  # superuser olmayan kullanıcı
            password = 'hako123'
            run_blog_tests(username, password)
        elif choice == '3':
            username = 'hako'  # input("Kullanıcı adını giriniz: ")
            password = 'hako123'  # input("Şifreyi giriniz: ")
            from .adminBlogTest import run_tests as run_admin_blog_tests
            run_admin_blog_tests(username, password)
        elif choice == '4':
            username = 'hako'  # input("Kullanıcı adını giriniz: ")
            password = 'hako123'  # input("Şifreyi giriniz: ")
            from .industryPage import run_industry_tests
            run_industry_tests(username, password)
        elif choice == '5':
            username = 'hako'  # input("Kullanıcı adını giriniz: ")
            password = 'hako123'  # input("Şifreyi giriniz: ")
            from .adminIndustriesTest import run_industry_tests
            run_industry_tests(username, password)
        elif choice == '6':
            username = input("Kullanıcı adını giriniz: ")
            password = input("Şifreyi giriniz: ")
            from .modalLoginTest import run_tests as run_login_tests
            run_login_tests(username, password)
        elif choice == '0':
            print("Çıkış yapılıyor...")
            return True # Çıkış seçeneği varsa döngüyü bitiriyoruz.

def main_menu():
    while True:
        print('**Bu testleri width:980px ve üzeri cihazlarda çalıştırınız.**')
        print("1- Ana Sayfa, Navigasyon ve imaj Testleri Çalıştır")
        print("2- Kullanıcı Blog Testleri Çalıştır")
        print("3- Admin Blog Testlerini Çalıştır (kapsamlı test)")
        print("4- Endüstri(Hizmet) Sayfaları Testleri Çalıştır")
        print("5- Admin Endüstri Testlerini Çalıştır (kapsamlı test)")
        print("6- Popup Login Testlerini Çalıştır")
        print("0- Çıkış")

        choice = input("Birden fazla test çalıştırmak için test numaralarını virgülle ayırarak giriniz (örneğin: 1,2,3): ")

        
        if choice:
            choices = choice.split(',')
            exit= run_selected_tests(choices)
            if exit==True:
                break
        else:
            print("Geçersiz giriş. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    main_menu()