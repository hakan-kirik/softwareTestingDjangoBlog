# Django ve Selenium ile Yazılım Test Projesi

Bu proje, Django ile geliştirilen bir web uygulamasının otomatik testlerini gerçekleştirmek için Selenium kullanmaktadır. Proje kapsamında, web uygulamasının ana sayfası, kullanıcı blogları ve endüstri sayfaları gibi çeşitli bileşenler üzerinde testler yazılmıştır.

## İçindekiler

- [Django ve Selenium ile Yazılım Test Projesi](#django-ve-selenium-ile-yazılım-test-projesi)
  - [İçindekiler](#i̇çindekiler)
  - [Gereksinimler](#gereksinimler)
  - [Kurulum ve Çalıştırma](#kurulum-ve-çalıştırma)
    - [1. Gerekli Dosyaların İndirilmesi](#1-gerekli-dosyaların-i̇ndirilmesi)
    - [2. Docker ve Docker Compose Kurulumu](#2-docker-ve-docker-compose-kurulumu)
    - [3. Projenin Çalıştırılması](#3-projenin-çalıştırılması)
  - [Testlerin Çalıştırılması](#testlerin-çalıştırılması)
    - [Test Menüsünün Kullanılması](#test-menüsünün-kullanılması)
    - [Menü Seçenekleri](#menü-seçenekleri)
  - [Yapılanlar ve Çalışma Prensibi](#yapılanlar-ve-çalışma-prensibi)
    - [Projenin Ana Bileşenleri](#projenin-ana-bileşenleri)
  - [Sorun Giderme](#sorun-giderme)
    - [PostgreSQL Bağlantı Problemleri](#postgresql-bağlantı-problemleri)
    - [Genel Sorunlar](#genel-sorunlar)

## Gereksinimler

- Python 3.8+
- Docker
- Docker Compose
- Selenium WebDriver (ChromeDriver)
- Django 4.x
- PostgreSQL

## Kurulum ve Çalıştırma

### 1. Gerekli Dosyaların İndirilmesi

Proje dosyalarını GitHub üzerinden ya da direkt olarak bilgisayarınıza indirebilirsiniz.

### 2. Docker ve Docker Compose Kurulumu

Docker ve Docker Compose yüklü değilse, aşağıdaki linklerden kurulumlarını yapabilirsiniz:

- Docker: [Docker Kurulumu](https://docs.docker.com/get-docker/)
- Docker Compose: [Docker Compose Kurulumu](https://docs.docker.com/compose/install/)

### 3. Projenin Çalıştırılması

Projenin kök dizininde aşağıdaki komutları çalıştırarak PostgreSQL ve Django uygulamasını başlatabilirsiniz:

```bash
docker compose up -d 

```

Testlerin Çalıştırılması
------------------------

### Test Menüsünün Kullanılması

Testleri çalıştırmak için aşağıdaki komutu kullanabilirsiniz:
<span style="color: red;">Dikkat: Testler modül olarak tanımlandığından, doğrudan bir Python dosyası gibi çalıştırılamazlar. Bunun yerine testleri çalıştırmak için aşağıdaki komutu kullanmalısınız:</span>

```bash
python -m tests.mainmenu 

```


Bu komut, size bir menü sunarak hangi testlerin çalıştırılacağını seçmenize olanak tanır. 

### Menü Seçenekleri

Menüdeki seçenekler şu şekildedir:

1.  Ana Sayfa, Navigasyon ve imaj Testleri Çalıştır
    
2.  Kullanıcı Blog Testleri Çalıştır

3.  Admin Blog Testlerini Çalıştır (kapsamlı test)
    
4.  Endüstri (Hizmet) Sayfaları Testleri Çalıştır
    
5.  Admin Endüstri Testlerini Çalıştır (kapsamlı test)
    
6.  Popup Login Testlerini Çalıştır
    

Birden çok test seçeneğini çalıştırmak için seçimlerinizi virgül ile ayırarak girebilirsiniz. Örneğin:

```plain
1,3,5 
```


Yapılanlar ve Çalışma Prensibi
------------------------------

### Projenin Ana Bileşenleri

*   **Ana Sayfa ve Navigasyon Testleri:** Ana sayfanın ve navigasyon linklerinin doğru çalıştığını kontrol eder.
    
*   **Kullanıcı Blog Testleri:** Blog ekleme, güncelleme ve silme işlemlerinin doğru çalıştığını ve web sayfasında görünümünü kontrol eder.
    
*   **Endüstri Sayfaları Testleri:** Endüstri sayfalarının eklenmesi, güncellenmesi ve silinmesini ve web sayfasında görünümünü kontrol eder.
    
*   **Popup Login Testleri:** Kullanıcı giriş işlemlerinin doğru çalıştığını kontrol eder.
    
*   **Admin Blog Testleri:** Admin paneli üzerinden blog ekleme, güncelleme, silme ve kolon kısıtlama işlemlerinin doğru çalıştığını kontrol eder.
    
*   **Admin Endüstri Testleri:** Admin paneli üzerinden endüstri ekleme, güncelleme , silme  ve kolon kısıtlama işlemlerinin doğru çalıştığını kontrol eder.
  

## Sorun Giderme


### PostgreSQL Bağlantı Problemleri

Eğer PostgreSQL veritabanına bağlanmada sorun yaşıyorsanız, aşağıdaki adımları izleyerek sorunu gidermeye çalışabilirsiniz:

1.  Docker konteynerlerinin düzgün bir şekilde çalıştığından emin olmak için aşağıdaki komutu kullanarak konteynerlerin durumunu kontrol edin
    
```bash
docker ps
```
2. PostgreSQL konteynerinin loglarını inceleyerek olası hata mesajlarını kontrol edebilirsiniz:
   
   ```bash 
        docker logs <postgre_container_id>
   ```

3. Django uygulamasının loglarını inceleyerek olası bağlantı sorunlarını tespit edebilirsiniz:

    ```bash
    docker logs <django_container_id>

    ```


    

### Genel Sorunlar

  **Konteynerler Başlamıyor:** Eğer konteynerler başlamıyorsa, docker compose up -d komutunu kullanarak yeniden başlatmayı deneyin.
   

    ```bash
    docker compose up -d 

    ```

  
    
  **Port Çakışmaları:** Uygulama veya veritabanı portlarında çakışma olup olmadığını kontrol edin. Gerekirse, docker-compose.yml dosyasında port numaralarını değiştirin.(port numaralarını değiştirdiğinizde testler düzgün çalışmayacaktır.)
