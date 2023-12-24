from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger, EmptyPage
from random import randint
import json
import time

from app.models import Post, Comment, Tag, Profile

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
    pass

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

def indexTagged(request, tag_name):
    data = {'tag': tag_name, 'posts': paginate(get_tagged_posts(tag_name), request), 'sidebar': get_sidebar()}
    return render(request, "index-tagged.html", data)

def post(request, post_id):
    if post_id >= len(get_all_posts()) or post_id < 0:
        request.status_code = 404
        data = {'message': '404 ERROR - POST NOT FOUND'}
        return render(request, "error.html", data)

    data = {'post': get_single_post(post_id), 'comments': paginate(get_comments_by_post(post_id), request, per_page=10), 'sidebar': get_sidebar()}
    return render(request, "post.html", data)

def login(request):
    data = {'sidebar': get_sidebar()}
    return render(request, "login.html", data)

def register(request):
    data = {'sidebar': get_sidebar()}
    return render(request, "register.html", data)

def addPost(request):
    data = {'sidebar': get_sidebar()}
    return render(request, "add-post.html", data)

def profile(request):
    data = {'sidebar': get_sidebar()}
    return render(request, "profile.html", data)