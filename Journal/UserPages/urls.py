from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name ="UserPages"
urlpatterns = [
    path("", views.index, name="index"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('sign-up/', views.sign_up, name = "sign_up"),
    path('create-entry/', views.create_entry, name = 'create-entry'),
    path('mod/', views.mod, name='mod')

  ]

handler403 = 'UserPages.views.custom_403'
handler404 = 'UserPages.views.custom_404'