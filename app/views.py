from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger, EmptyPage
from random import randint
import json
import time
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from app.models import Post, Comment, Tag, Profile
from app.forms import LoginoForm, RegisterForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db import IntegrityError

def get_comments_by_post(post_id):
    return Comment.objects.get_by_post(post_id)

def get_all_posts():
    posts_arr = Post.objects.sort_by_date()
    posts = []
    for post in posts_arr:
        # posts.append({'id': post.id, 'author': post.author, 'rating': post.rating, 'title': post.title, 'text': post.text, 'tags': post.tags.all(), 'comments': get_comments_by_post(post.id)})
        posts.append({'data': post, 'comments': get_comments_by_post(post.id)})

    return posts

def get_hot_posts():
    posts_arr = Post.objects.sort_by_hot()
    posts = []
    for post in posts_arr:
        # posts.append({'id': post.id, 'author': post.author, 'rating': post.rating, 'title': post.title, 'text': post.text, 'tags': post.tags.all(), 'comments': get_comments_by_post(post.id)})
        posts.append({'data': post, 'comments': get_comments_by_post(post.id)})

    return posts

def get_tagged_posts(tag):
    posts_arr = Post.objects.get_by_tag(tag)
    posts = []
    for post in posts_arr:
        posts.append({'data': post, 'comments': get_comments_by_post(post.id)})

    return posts

def get_single_post(post_id):
    post = Post.objects.get_by_id(post_id)
    return {'data': post}

def get_sidebar():
    return {
        'popular_tags': Tag.objects.get_popular_tags(),
        'top_members': Profile.objects.get_popular_members()
    }

def paginate(objects, request, per_page=5):
    page = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    
    try:
        page = paginator.page(page)
    except (InvalidPage, PageNotAnInteger, EmptyPage) as e:
        page = paginator.page(1)

    return page

# Create your views here.
def index(request):
    data = {'posts': paginate(get_all_posts(), request), 'sidebar': get_sidebar()}
    return render(request, "index.html", data)

def indexhot(request):
    data = {'posts': paginate(get_hot_posts(), request), 'sidebar': get_sidebar()}
    return render(request, "index.html", data)

def indexTagged(request, tag_name):
    data = {'tag': tag_name, 'posts': paginate(get_tagged_posts(tag_name), request), 'sidebar': get_sidebar()}
    return render(request, "index-tagged.html", data)

def post(request, post_id):
    try:
        if post_id < 0:
            raise Exception("Post id out of range")
        post = get_single_post(post_id)
    except:
        request.status_code = 404
        data = {'message': '404 ERROR - POST NOT FOUND'}
        return render(request, "error.html", data)
    
    if request.method == "GET":
        comment_form = CommentForm()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        try:
            comment_form.save(request)
            return redirect(request.path)
        except:
            comment_form.add_error(None, 'Something went wrong during saving post')

    data = {'post': post, 'comments': paginate(get_comments_by_post(post_id), request, per_page=10), 'sidebar': get_sidebar(), 'form': comment_form}
    return render(request, "post.html", data)

@csrf_protect
def login(request):
    if request.method == "GET":
        login_form = LoginoForm()
    if request.method == "POST":
        login_form = LoginoForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                dj_login(request, user)
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, 'Incorrect login or password')
        
    data = {'sidebar': get_sidebar(), 'form': login_form}
    return render(request, "login.html", data)

@csrf_protect
def register(request):
    if request.method == "GET":
        register_form = RegisterForm()
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            try:
                user = register_form.save()
                dj_login(request, user)
                return redirect(reverse('index'))
            except IntegrityError:
                register_form.add_error(None, 'User already exists')
            except AttributeError:
                pass

    data = {'sidebar': get_sidebar(), 'form': register_form}
    return render(request, "register.html", data)

@login_required(login_url='login')
def logout(request):
    dj_logout(request)
    return redirect(reverse('login'))

@login_required(login_url="login", redirect_field_name="continue")
def addPost(request):
    if request.method == "GET":
        post_form = PostForm()
    if request.method == "POST":
        post_form = PostForm(request.POST)
    if post_form.is_valid():
        try:
            post_id = post_form.save(request)
            return redirect('post', post_id=post_id)
        except:
            post_form.add_error(None, 'Something went wrong during saving post')

    data = {'sidebar': get_sidebar(), 'form': post_form}
    return render(request, "add-post.html", data)

@login_required(login_url="login", redirect_field_name="continue")
def profile(request):
    data = {'sidebar': get_sidebar()}
    return render(request, "profile.html", data)