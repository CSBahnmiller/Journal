from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate, views as auth_views
from .forms import RegisterForm, UserContentForm
from django.contrib.auth.models import User, Group
from .models import UserContent

# Create your views here.


@login_required(login_url="../../UserPages/login")
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
                    group.user_set_add(user)
                except:
                    pass
    return render(request, 'UserPages/index.html', {'posts': posts})

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
    return auth_views.logout_then_login(request, login_url='../../UserPages/login')




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



   


