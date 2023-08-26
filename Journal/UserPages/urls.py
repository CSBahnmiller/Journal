from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views


app_name ="UserPages"
urlpatterns = [
    path("", views.index, name="index"),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('password/', auth_views.PasswordChangeView.as_view(template_name="registration/change-password.html")),
    path("login/", views.Login_View.as_view(template_name="registration/login.html"), name = 'login'),
    path('password/', views.PasswordsChangeView.as_view(template_name="registration/change-password.html"), name='reset-password'),
    path('password-success/', views.password_success, name = "password_success"),
    path('logout/', views.logout_request, name='logout'),
    path('sign-up/', views.sign_up, name = "sign_up"),
    path('create-entry/', views.create_entry, name = 'create-entry'),
    path('mod/', views.mod, name='mod'),
    path('edit-entry/<str:pk>/', views.edit_entry, name = 'update_entry'),
    path('404/', views.error404, name = 'error'),

  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'UserPages.views.custom_403'
handler404 = 'UserPages.views.custom_404'