from django.urls import path

from .views import index
from .views import other_page
from .views import BVLoginView
from .views import BVLogoutView
from .views import profile
from .views import ChangeUserInfoView
from .views import BVPasswordChangeView
from .views import RegisterUserView, RegisterDoneView
from .views import user_activate
from .views import DeleteUserView
from .views import by_rubric
from .views import detail
from .views import profile_bv_detail
from .views import profile_bv_add
from .views import profile_bv_change, profile_bv_delete


app_name = 'main'
urlpatterns = [
    path('<int:rubric_pk>/<int:pk>', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),#страница под и над рубрик
    path('<str:page>/', other_page, name='other'),#Главная
    path('accounts/login/', BVLoginView.as_view(), name='login'),#страница входа
    path('accounts/profile/change/<int:pk>', profile_bv_change, name='profile_bv_change'),#страница изменения объявы
    path('accounts/profile/delete/<int:pk>', profile_bv_delete, name='profile_bv_delete'),#страница удаления объявы
    path('accounts/profile/add/', profile_bv_add, name='profile_bv_add'),#старница добавления объявления
    path('accounts/profile/<int:pk>/', profile_bv_detail, name='profile_bv_detail'),#список объявлений зарегиного пользователя
    path('accounts/profile/', profile, name='profile'),#страница профиля
    path('accounts/logout/', BVLogoutView.as_view(), name='logout'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),#страница изменения данных пользователя
    path('accounts/password/change/', BVPasswordChangeView.as_view(), name='password_change'),#страница смены пароля
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),#страница успешной регитсрации
    path('accounts/register/', RegisterUserView.as_view(), name='register'),#страница регистрации
    path('accounts/register/activate/<str:sign>', user_activate, name='register_activate'),#страница активирован
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),#удаление пользователя
    path('', index, name='index'),#маршрут уровня приложения
]