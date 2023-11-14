from django.shortcuts import render

POSTS = [
    {
        'id': i,
        'title': f'Post N{i}',
        'text': 'ara ARA '*5*i
    } for i in range(0,8)
]

# Create your views here.
def index(request):
    return render(request, "index.html", {'posts': POSTS})

def indexTagged(request):
    return render(request, "index-tagged.html", {'posts': POSTS})

def post(request, post_id):
    item = POSTS[post_id]
    return render(request, "post.html", {'post': item})

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def addPost(request):
    return render(request, "add-post.html")

def profile(request):
    return render(request, "profile.html")