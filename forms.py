# artist_profile/forms.py
from django import forms
from .models import Post, Comment,Profile,User,CartItem

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['artist','art_name','category','image','price' ,'caption', ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'username', 'user_pic', 'bio']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user

class AddToCartForm(forms.Form):
        art_name = forms.CharField(max_length=100, required=True)
        price = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
        image = forms.ImageField(required=True)

