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
import requests


#Import Pagination Stuff
from django.core.paginator import Paginator


#Code to grab API Quote

def get_random_quote():
    api_url = "https://zenquotes.io/api/random"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        
        if data and isinstance(data, list):
            quote_data = data[0]
            quote = quote_data.get("q", "")
            author = quote_data.get("a", "")
            html_quote = quote_data.get("h", "")
            
            return {
                "quote": quote,
                "author": author,
                "html_quote": html_quote
            }
            
    except Exception as e:
        print("An error occurred:", e)
        return None





# Create your views here.


@login_required(login_url="../../UserPages/login/")
def index(request):

    posts = UserContent.objects.filter(author=request.user)

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

    # Initialize the paginator
    paginator = Paginator(posts, 5)  # Show 5 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

#Adding API Quote
    quote_data = get_random_quote()
    context = {}
    
    if quote_data:
        quote = quote_data["quote"]
        author = quote_data["author"]
        html_quote = quote_data["html_quote"]
        context["quote"] = quote
        context["author"] = author
        context["html_quote"] = html_quote


#End of API Quote


    
    context.update({'posts': posts, 'postFilter': postFilter, 'page_obj': page_obj})
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

        # Initialize the paginator
    paginator = Paginator(posts, 5)  # Show 5 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'posts': posts, 'postFilter' : postFilter, 'page_obj': page_obj }
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




   


