from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate, views as auth_views
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from .forms import RegisterForm, UserContentForm, PasswordChangingFrom, LoginForm
from django.contrib.auth.models import User, Group
from .models import UserContent
from .filters import EntryFilter

# Create your views here.


@login_required(login_url="../../UserPages/login/")
def index(request):
    posts = UserContent.objects.all()

    if request.method == 'POST':
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")
        if post_id:
            post = UserContent.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("UserPages.delete_post")):
                post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set_remove(user)
                except:
                    pass
                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass
    postFilter = EntryFilter(request.GET, queryset=posts)
    posts = postFilter.qs
    
    context = {'posts': posts, 'postFilter' : postFilter}
    return render(request, 'UserPages/index.html', context)

@login_required(login_url="../../UserPages/login")
@permission_required("UserPages.delete_usercontent", login_url="../../UserPages/login", raise_exception=True)
def mod(request):
    posts = UserContent.objects.all()

    if request.method == 'POST':
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")
        if post_id:
            post = UserContent.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("UserPages.delete_usercontent")):
                post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass
                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass
    
    postFilter = EntryFilter(request.GET, queryset=posts)
    posts = postFilter.qs
    
    context = {'posts': posts, 'postFilter' : postFilter}
    return render(request, 'UserPages/mod.html', context)


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('../../UserPages/')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {"form": form})

def logout_request(request):
    return auth_views.logout_then_login(request, login_url=reverse_lazy("UserPages:login"))




@login_required(login_url="../../UserPages/login")
@permission_required("UserPages.add_usercontent", login_url="../../UserPages/login", raise_exception=True)
def create_entry(request):
    if request.method == 'POST':
        
        form = UserContentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('../../UserPages/')
    else:
        form = UserContentForm()
    return render(request, 'UserPages/create-entry.html', {"form" : form})


@login_required(login_url="../../UserPages/login")
@permission_required("UserPages.add_usercontent", login_url="../../UserPages/login", raise_exception=True)
def edit_entry(request, pk):

    entry = UserContent.objects.get(id=pk)
    form = UserContentForm(instance=entry)

    if request.method == 'POST':
        form = UserContentForm(request.POST, instance=entry)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('../../../UserPages/') 
    
    context = {'form':form}
    return render(request,'UserPages/edit-entry.html', context) 


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingFrom
    #form_class = PasswordChangeForm
    success_url = reverse_lazy('UserPages:password_success')

def password_success(request):
    return render(request, 'registration/password_success.html', {})

class Login_View(LoginView):
    form_class = LoginForm
    success_url = reverse_lazy("UserPages:index")




def error404(request):
    return render(request, 'UserPages/404.html')

def custom_404(request, exception):
    return render(request, 'UserPages/404.html', status=404)

def custom_403(request, exception):
    return render(request, 'UserPages/403.html', status=403)




   


