
from django import forms

from blog.models import CustomUser


class RegisterForm(forms.Form):
    username = forms.CharField(label='Kullanıcı Adı', error_messages={'required': 'Kullanıcı adı alanı zorunludur.'})
    email = forms.EmailField(label='E-posta', error_messages={'required': 'E-posta alanı zorunludur.'})
    password1 = forms.CharField(label='Şifre', widget=forms.PasswordInput, error_messages={'required': 'Şifre alanı zorunludur.'})
    password2 = forms.CharField(label='Şifreyi Onayla', widget=forms.PasswordInput,
                                error_messages={'required': 'Şifre onayı alanı zorunludur.'})

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu kullanıcı adı zaten kullanımda.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-posta adresi zaten kullanımda.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Şifreler uyuşmuyor.")
        return password2