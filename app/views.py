from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")

def indexTagged(request):
    return render(request, "index-tagged.html")

def post(request):
    return render(request, "post.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def addPost(request):
    return render(request, "add-post.html")

def profile(request):
    return render(request, "profile.html")