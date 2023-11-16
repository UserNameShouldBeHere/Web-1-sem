from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger, EmptyPage

POSTS = [
    {
        'id': i,
        'title': f'Post N{i}',
        'text': 'ara ARA '*5*i
    } for i in range(1,35)
]

COMMENTS = [
    {
        'id': i,
        'text': 'pam PARAM '*5*i
    } for i in range(1,20)
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
    data = {'posts': paginate(POSTS, request), 'sidebar': SIDEBAR[0]}
    return render(request, "index.html", data)

def indexTagged(request, tag_name):
    data = {'tag': tag_name, 'posts': paginate(POSTS, request), 'sidebar': SIDEBAR[0]}
    return render(request, "index-tagged.html", data)

def post(request, post_id):
    if post_id >= len(POSTS) or post_id < 0:
        request.status_code = 404
        data = {'message': '404 ERROR - POST NOT FOUND'}
        return render(request, "error.html", data)

    data = {'post': POSTS[post_id], 'comments': paginate(COMMENTS, request, 10), 'sidebar': SIDEBAR[0]}
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