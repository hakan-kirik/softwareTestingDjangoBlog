from django import forms
from blog.models import Industry


class IndustryForm(forms.ModelForm):
    class Meta:
        model = Industry
        fields = ['user', 'name', 'image', 'icon_class', 'content', 'subdescription']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 100:
            raise forms.ValidationError('Ensure this value has at most 100 characters (it has {}).'.format(len(name)))
        return name

    def clean_icon_class(self):
        icon_class = self.cleaned_data.get('icon_class')
        if len(icon_class) > 50:
            raise forms.ValidationError('Ensure this value has at most 50 characters (it has {}).'.format(len(icon_class)))
        return icon_class

    def clean_subdescription(self):
        subdescription = self.cleaned_data.get('subdescription')
        if len(subdescription) > 255:
            raise forms.ValidationError('Ensure this value has at most 255 characters (it has {}).'.format(len(subdescription)))
        return subdescription

    def clean_user(self):
        print('bak bu calisuuyo')
        user = self.cleaned_data.get('user')
        if user is None:
            raise forms.ValidationError('This field cannot be null.')
        return user