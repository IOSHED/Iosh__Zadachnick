from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.views import View

from ..models import CustomUser

# TODO: use regex in 're'


class CheckEmailView(View):
    @staticmethod
    def post(request):
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email).exists():
            return HttpResponse('This email already exists')
        return HttpResponse('')


class CheckHaveEmailView(View):
    @staticmethod
    def post(request):
        email = request.POST.get('username')
        if not CustomUser.objects.filter(email=email).exists():
            return HttpResponse('There is no user with this email address')
        return HttpResponse('')


class CheckPasswordView(View):
    @staticmethod
    def post(request):
        password1: str = request.POST.get('password1')
        if password1 is None:
            password1 = request.POST.get('password')

        if len(password1) < 8:
            return HttpResponse('The password must contain 8 characters')
        if password1.isnumeric():
            return HttpResponse('The password must contain Latin letters and numbers')
        if not any(c.isupper() for c in password1):
            return HttpResponse('The password must contain uppercase Latin letters')
        return HttpResponse('')


class CheckRePasswordView(View):
    @staticmethod
    def post(request):
        password1: str = request.POST.get('password1')
        password2: str = request.POST.get('password2')
        if password1 == password2:
            return HttpResponse('')
        return HttpResponse('Passwords must match')


class CheckLoginUser(View):
    @staticmethod
    def post(request):
        email = request.POST.get('username')
        raw_password = request.POST.get('password')
        if authenticate(email=email, password=raw_password) is None:
            return HttpResponse('Invalid username or password')
        return HttpResponse('')
