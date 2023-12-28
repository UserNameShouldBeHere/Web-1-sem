from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from app.models import Post, Comment, Tag, Profile
from django.core.validators import validate_email

class LoginoForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'row p-2 fs-6',
        'placeholder': 'awesome@mail.ru',
        'required': 'true'
    }))

    password = forms.CharField(min_length=5, widget=forms.TextInput(attrs={
        'class': 'row p-2 fs-6',
        'required': 'true',
        'placeholder': '',
        'type': 'password',
        'required': 'true'
    }))

    # def clean_password(self):
    #     data = self.cleaned_data['password']
    #     if data == 'ahaha':
    #         raise ValidationError('No ahaha pls')
    #     return data

class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'row p-2 fs-6',
        'placeholder': 'awesome@mail.ru',
        'required': 'true'
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'row p-2 fs-6',
        'placeholder': 'Ahmed',
        'required': 'true'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'row p-2 fs-6',
        'placeholder': 'Abdulaev',
        'required': 'true'
    }))

    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'row p-2 fs-6',
        'required': 'true',
        'placeholder': '',
        'type': 'password',
        'required': 'true'
    }))

    repeat_password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'row p-2 fs-6',
        'required': 'true',
        'placeholder': '',
        'type': 'password',
        'required': 'true'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']

    def clean(self):
        first_password = self.cleaned_data['password']
        second_password = self.cleaned_data['repeat_password']
        if first_password != second_password:
            raise ValidationError('Passwords dont match')
        
    def save(self, **kwargs):
        self.cleaned_data.pop('repeat_password')
        user = User.objects.create_user(**self.cleaned_data)
        # user = User.objects.create_user(username=self.cleaned_data['username'], first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'], password=self.cleaned_data['password'])
        profile = Profile(user=user)
        profile.save()
    
class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=250, widget=forms.TextInput(attrs={
        'class': 'col fs-6',
        'placeholder': 'Awesome title',
        'required': 'true'
    }))

    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'col fs-6 post-text',
        'required': 'true',
        'placeholder': 'Some text',
        'required': 'true'
    }))

    tags = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'col fs-6',
        'placeholder': 'C++, Database, ...'
    }), required=False)

    class Meta:
        model = Post
        fields = ['title', 'text', 'tags']

    def save(self, request, **kwargs):
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']
        author = Profile.objects.get_by_user_id(request.user.id).id
        tags = [tag.strip() for tag in self.cleaned_data['tags'].split(',') if tag.strip()]
        saved_tags = []
        for tag in tags:
            saved_tag, _ = Tag.objects.get_or_create(name=tag)
            saved_tags.append(saved_tag)
        
        post = Post(title=title, text=text, author_id=author)
        post.save()

        post.tags.set(saved_tags)
        post.save()

        return post.id

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'col fs-6 comment-text',
        'required': 'true',
        'placeholder': 'Your comment'
    }))

    class Meta:
        model = Post
        fields = ['text']

    def save(self, request, **kwargs):
        text = self.cleaned_data['text']
        author = Profile.objects.get_by_user_id(request.user.id).id
        post = Post.objects.get_by_id(int(request.path[request.path.rfind('/')+1:])).id

        comment = Comment(text=text, author_id=author, post_id=post)
        comment.save()

# class ProfileForm(forms.ModelForm):
#     class Meta