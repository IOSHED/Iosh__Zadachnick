from django.urls import path

from .views import CreateUserView, LoginUserView, CheckEmailView, CheckPasswordView, CheckRePasswordView, \
    CreateInfoUserView, LogoutUserView, DeleteUserView, UpdateUserView, CheckHaveEmailView, CheckLoginUser, LoadImage

urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('create-info-user/<int:pk>', CreateInfoUserView.as_view(), name='create-info-user'),
    path('login-user/', LoginUserView.as_view(), name='login-user'),
    path('logout-user/', LogoutUserView.as_view(), name='logout-user'),
    path('delete-user/', DeleteUserView.as_view(), name='delete-user'),
    path('update-user/', UpdateUserView.as_view(), name='update-user'),
    path('load-icon/', LoadImage.as_view(), name='load-icon')


    # TODO: add forgot password
    # TODO: add view ditail
    # TODO: add activate email
]

htmx_patterns = [
    path('check-email/', CheckEmailView.as_view(), name='check-email'),
    path('check-password/', CheckPasswordView.as_view(), name='check-password'),
    path('check-re-password/', CheckRePasswordView.as_view(), name='check-re-password'),
    path('check-have-email/', CheckHaveEmailView.as_view(), name='check-have-email'),
    path('check-login-user/', CheckLoginUser.as_view(), name='check-login-user')
]

urlpatterns += htmx_patterns
