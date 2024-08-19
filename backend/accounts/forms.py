from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from PIL import Image as PILImage
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class InfoUserForm(forms.ModelForm):
    name = forms.CharField(min_length=3, max_length=64)
    surname = forms.CharField(min_length=3, max_length=64)

    class Meta:
        model = CustomUser
        fields = ('name', 'surname', 'birthday_at')


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'surname', 'birthday_at')


class LoadImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('icon64', 'icon32')

    def clean_image(self):
        image = self.cleaned_data.get('icon64')
        img = PILImage.open(image)

        expected_size_img = (64, 64)

        if img.size == expected_size_img:
            return image
        return img.resize(expected_size_img)
