from django.shortcuts import render
from django.core.paginator import Paginator

POSTS = [
    {
        'id': i,
        'title': f'Post N{i}',
        'text': 'ara ARA '*5*i
    } for i in range(0,35)
]

SIDEBAR = [
    {
        'popular_tags': [
            {
                'id': 1,
                'name': 'C++'
            },
            {
                'id': 2,
                'name': 'Brainfuck'
            },
            {
                'id': 3,
                'name': 'Python'
            },
            {
                'id': 4,
                'name': 'Rust'
            },
            {
                'id': 5,
                'name': 'Kotlin'
            },
            {
                'id': 6,
                'name': 'Java'
            }
        ],
        'top_members': [
            {
                'id': 1,
                'name': 'me'
            },
            {
                'id': 2,
                'name': 'Nagibator228'
            },
            {
                'id': 3,
                'name': 'UltraMegaCringe'
            },
            {
                'id': 4,
                'name': 'Abobus'
            },
            {
                'id': 5,
                'name': 'Aristotel'
            }
        ]
    }
]

def paginate(objects, page, per_page=5):
    paginator = Paginator(POSTS, per_page)
    
    try:
        page = paginator.page(page)
    except Exception:
        page = paginator.page(1)

    return page

# Create your views here.
def index(request):
    page = request.GET.get('page', 1)
    data = {'posts': paginate(POSTS, page), 'sidebar': SIDEBAR[0]}
    return render(request, "index.html", data)

def indexTagged(request, tag_name):
    page = request.GET.get('page', 1)
    data = {'tag': tag_name, 'posts': paginate(POSTS, page), 'sidebar': SIDEBAR[0]}
    return render(request, "index-tagged.html", data)

def post(request, post_id):
    if post_id >= len(POSTS) or post_id < 0:
        request.status_code = 404
        data = {'message': '404 ERROR - POST NOT FOUND'}
        return render(request, "error.html", data)

    data = {'post': POSTS[post_id], 'sidebar': SIDEBAR[0]}
    return render(request, "post.html", data)

def login(request):
    data = {'sidebar': SIDEBAR[0]}
    return render(request, "login.html", data)

def register(request):
    data = {'sidebar': SIDEBAR[0]}
    return render(request, "register.html", data)

def addPost(request):
    data = {'sidebar': SIDEBAR[0]}
    return render(request, "add-post.html", data)

def profile(request):
    data = {'sidebar': SIDEBAR[0]}
    return render(request, "profile.html", data)