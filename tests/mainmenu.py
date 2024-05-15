def main_menu():
    print("1- Ana Sayfa ve Navigasyon Testleri Çalıştır")
    print("2- Blog Testleri Çalıştır")
    print("3- Endüstri Sayfaları Testleri Çalıştır")
    print("4- Popup ve İmaj Kontrol Testleri Çalıştır")
    choice = input("Lütfen test numarasını giriniz: ")
    if choice == '1':
        from .testhomepage import run_tests as run_home_tests
        run_home_tests()
    elif choice == '2':
        # Blog Testlerini burada çağır
        pass
    elif choice == '3':
        # Endüstri Sayfaları Testlerini burada çağır
        pass
    elif choice == '4':
        # Popup ve İmaj Kontrol Testlerini burada çağır
        pass
    else:
        print("Geçersiz seçim.")

if __name__ == "__main__":
    main_menu()
