from PIL import Image as PILImage
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, UpdateView

from ..forms import CustomUserCreationForm, CustomAuthenticationForm, InfoUserForm, UpdateUserForm, LoadImageForm
from ..models import CustomUser


class CreateUserView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_email_verification = False
        user.save()

        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')

        user = authenticate(email=email, password=raw_password)

        login(self.request, user)

        return redirect('create-info-user', pk=user.id, permanent=True)


class LoginUserView(FormView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/registration/login.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=raw_password)

        # login(self.request, user)
        # return redirect('home', permanent=True)
        if user is not None:
            login(self.request, user)
            print(f"User {user.email} has logged in successfully.")
        else:
            print("Authentication failed.")
        return redirect('home', permanent=True)


@method_decorator(login_required, name='dispatch')
class CreateInfoUserView(UpdateView):
    model = CustomUser
    form_class = InfoUserForm
    template_name = 'accounts/registration/create_info_user.html'

    def form_valid(self, form):
        form.save()
        return redirect('home', permanent=True)


@method_decorator(login_required, name='dispatch')
class LogoutUserView(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect('home', permanent=True)


@method_decorator(login_required, name='dispatch')
class DeleteUserView(View):
    @staticmethod
    def post(request):
        request.user.is_active = False
        return redirect('home', permanent=True)


@method_decorator(login_required, name='dispatch')
class UpdateUserView(UpdateView):
    model = CustomUser
    form_class = UpdateUserForm
    template_name = 'accounts/users/update_user.html'

    def form_valid(self, form):
        form.save()
        return redirect('home', permanent=True)


class LoadImage(FormView):
    form_class = LoadImageForm

    def form_valid(self, form):
        img = PILImage.open(form.cleaned_data['icon64'])
        form.cleaned_data['icon32'] = img.resize((32, 32))
        form.save()
