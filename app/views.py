from django.shortcuts import render

POSTS = [
    {
        'id': i,
        'title': f'Post N{i}',
        'text': 'ara ARA '*5*i
    } for i in range(0,8)
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

# Create your views here.
def index(request):
    data = {'posts': POSTS, 'sidebar': SIDEBAR[0]}
    return render(request, "index.html", data)

def indexTagged(request, tag_name):
    data = {'tag': tag_name, 'posts': POSTS, 'sidebar': SIDEBAR[0]}
    return render(request, "index-tagged.html", data)

def post(request, post_id):
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