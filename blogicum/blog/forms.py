from django import forms
from .models import Post, Comment
from django.contrib.auth import get_user_model


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author',)
        widgets = {
            'pub_date':  forms.DateTimeInput(
                format=("%Y-%m-%d %H:%M:%S"),
                attrs={'type': 'datetime-local'}
            )
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
