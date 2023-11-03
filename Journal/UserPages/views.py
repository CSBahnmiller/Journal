from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate, views as auth_views
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse, reverse_lazy, resolve
from .forms import RegisterForm, UserContentForm, CommentContentForm, PasswordChangingFrom, LoginForm
from django.contrib.auth.models import User, Group
from .models import UserContent, Comments, SharedPost
from .filters import EntryFilter, ModEntryFilter
import requests
import random


#Import Pagination Stuff
from django.core.paginator import Paginator


#Code to grab API Quote

# Code to grab API Quote
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
        else:
            return {
                "quote": "Too many requests. Obtain an auth key for unlimited access.",
                "author": "API Error",
                "html_quote": ""
            }
            
    except Exception as e:
        print("An error occurred:", e)
        # Return one of the specified phrases when an error occurs
        phrases = [
            "Life is like a box of chocolates, you never know what you are going to get.",
            "If at first you don't succeed, I don't recommend skydiving.",
            "If life gives you lemons, sell them and make a profit."
        ]
        random_phrase = random.choice(phrases)
        return {
            "quote": random_phrase,
            "author": "Unknown",
            "html_quote": ""
        }






# Create your views here.


@login_required(login_url=reverse_lazy('UserPages:login'))
def index(request):
    order = request.GET.get('order', 'desc')  # Default to descending order

    posts = UserContent.objects.filter(author=request.user).order_by('-created_at')
    
    # Apply filters if provided
    postFilter = EntryFilter(request.GET, queryset=posts)
    posts = postFilter.qs

    # Apply ordering based on the selected order
    order = request.GET.get('order', 'desc')  # Default to descending order

    if order == 'asc':
        posts = posts.order_by('created_at')
    else:
        posts = posts.order_by('-created_at')

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

    # Initialize the paginator
    paginator = Paginator(posts, 3)  # Show 3 posts per page

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

    comment_forms = {}  # Create a dictionary to hold comment forms for each post

    for post in posts:
        if request.method == 'POST':
            form = CommentContentForm(request.POST)  # Create a comment form instance for each post
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post  # Assign the comment to the post
                comment.save()
        else:
            form = CommentContentForm()  # Create an empty comment form

        comment_forms[post.id] = form  # Store the form in the dictionary with the post's ID as the key


    context.update({'posts': posts, 'postFilter': postFilter, 'page_obj':page_obj, 'comment_forms': comment_forms, 'form': form })
    return render(request, 'UserPages/index.html', context)

@login_required(login_url=reverse_lazy('UserPages:login'))
def shared_posts(request):
    shared_posts = SharedPost.objects.filter(recipient=request.user)
    form = CommentContentForm()  # Create an empty comment form for shared posts
    context = {'shared_posts': shared_posts, 'form': form}
    return render(request, 'UserPages/shared_posts.html', context)





@login_required(login_url=reverse_lazy('UserPages:login'))  # Use the appropriate URL name for the login page
@permission_required("UserPages.delete_usercontent", login_url=reverse_lazy('UserPages:login'), raise_exception=True)
def mod(request):
    order = request.GET.get('order', 'desc')  # Default to descending order
    posts = UserContent.objects.all().order_by('-created_at')

    
    # Apply filters if provided
    postFilter = ModEntryFilter(request.GET, queryset=posts)
    posts = postFilter.qs

    # Apply ordering based on the selected order
    order = request.GET.get('order', 'desc')  # Default to descending order

    if order == 'asc':
        posts = posts.order_by('created_at')
    else:
        posts = posts.order_by('-created_at')





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
    
    # postFilter = ModEntryFilter(request.GET, queryset=posts)
    # posts = postFilter.qs

    # Initialize the paginator
    paginator = Paginator(posts, 3)  # Show 3 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'posts': page_obj, 'postFilter': postFilter, 'page_obj': page_obj}
    return render(request, 'UserPages/mod.html', context)




def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse_lazy("UserPages:index"))
            #return redirect('../../UserPages/')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {"form": form})

def logout_request(request):
    return auth_views.logout_then_login(request, login_url=reverse_lazy("UserPages:login"))




@login_required(login_url="../../UserPages/login")
@permission_required("UserPages.add_usercontent", login_url="../../UserPages/login", raise_exception=True)
def create_entry(request):
    if request.method == 'POST':
        
        form = UserContentForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            return redirect(reverse_lazy('UserPages:index'))
    else:
        form = UserContentForm()
    return render(request, 'UserPages/create-entry.html', {"form" : form})



@login_required(login_url="../../UserPages/login")
@permission_required("UserPages.add_usercontent", login_url="../../UserPages/login", raise_exception=True)
def create_comment(request, pk):
    post = UserContent.objects.get(pk=pk)

    if request.method == 'POST':
        form = CommentContentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post  # Assign the comment to the post
            comment.save()
            return redirect('UserPages:index')

    return render(request, 'UserPages/post_detail.html', {'form': form, 'post': post})

def post_detail(request, pk):
    post = get_object_or_404(UserContent, pk=pk)
    return render(request, 'UserPages/post_detail.html', {'post': post})


@login_required(login_url=reverse_lazy('UserPages:login'))
@permission_required("UserPages.add_usercontent", login_url=reverse_lazy('UserPages:login'), raise_exception=True)
def edit_entry(request, pk):

    entry = UserContent.objects.get(id=pk)
    form = UserContentForm(instance=entry)

    if request.method == 'POST':
        form = UserContentForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            return redirect(reverse_lazy('UserPages:index')) 
    
    context = {'form':form}
    return render(request,'UserPages/edit-entry.html', context) 


@login_required(login_url=reverse_lazy('UserPages:login'))
@permission_required("UserPages.add_usercontent", login_url=reverse_lazy('UserPages:login'), raise_exception=True)
def edit_comment(request, pk):

    entry = Comments.objects.get(id=pk)
    form = CommentContentForm(instance=entry)

    if request.method == 'POST':
        form = CommentContentForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            return redirect(reverse_lazy('UserPages:index')) 
    
    context = {'form':form}
    return render(request,'UserPages/edit-comment.html', context) 



@login_required(login_url=reverse_lazy('UserPages:login'))  # Use the appropriate URL name for the login page
@permission_required("UserPages.delete_usercontent", login_url=reverse_lazy('UserPages:login'), raise_exception=True)
def delete_post(request, pk1, pk2):

    entry = UserContent.objects.get(id=pk1)
    entry.delete()
    if pk2 == 1:
        return redirect('UserPages:index')
    elif pk2 == 2:
        return redirect('UserPages:mod')
    else:
        return redirect('Main:home')
    
   

@login_required(login_url=reverse_lazy('UserPages:login'))  # Use the appropriate URL name for the login page
@permission_required("UserPages.delete_usercontent", login_url=reverse_lazy('UserPages:login'), raise_exception=True)
def delete_comment(request, pk1, pk2):

    comment = Comments.objects.get(id=pk1)
    comment.delete()
    if pk2 == 1:
        return redirect('UserPages:index')
    elif pk2 == 2:
        return redirect('UserPages:mod')
    else:
        return redirect('Main:home')



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

def custom_500(request):
    return render(request, 'UserPages/500.html', status=500)




   


