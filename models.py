# artist_profile/models.py
from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    FullName=models.CharField(max_length=100,blank=False)
    DateOfBirth=models.DateField(blank=False)
    Gender_choices =( ("Male","M"),("Female","F"),("Other","O") )
    Gender=models.CharField(max_length=10,blank=False,choices=Gender_choices)
    Username=models.CharField(max_length=100,blank=False,primary_key=True,unique=True)
    MobileNumber = models.CharField(max_length=20, blank=False, unique=True)
    Email = models.CharField(max_length=100, blank=False, unique=True)
    password = models.CharField(max_length=100, blank=False )

    TypeOfArtist_choices=( ("Aesthetic drawings","Aesthetic drawings") , ("Traditional Arts","Traditional Arts") , ("Sculptures Arts","Sculptures Arts"), ("Anime/Manga Arts","Anime/Manga Arts") , ("Real life Drawings","Real life Drawings"), ("Doodle Art","Doodle Art") , ("Pen Drawings","Pen Drawings") , ("Nature Arts","Nature Arts") )
    TypeOfArtist = models.CharField(max_length=100, blank=False,choices=TypeOfArtist_choices)

    class Meta:
        db_table = "artist_table"

    def __str__(self):
        return self.Username

class ArtistProfile(models.Model):
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=False, primary_key=True, unique=True, default='user2086')

    artist_pic = models.ImageField(upload_to='artist_pics/', default='static/user_profiles/userpic.png')
    bio = models.TextField(default='Add Bio✏️')
    social_media = models.CharField(max_length=100, blank=True)
    # Add other fields to store information about the artist's profile

    class Meta:
        db_table = "artistprofile_table"
    def __str__(self):
        return self.artist.Username
class Post(models.Model):
    art_name=models.CharField(max_length=100,blank=False)
    category_choice=( ("Aesthetic drawings","Aesthetic drawings") , ("Traditional Arts","Traditional Arts") , ("Sculptures Arts","Sculptures Arts"), ("Anime/Manga Arts","Anime/Manga Arts") , ("Real life Drawings","Real life Drawings"), ("Doodle Art","Doodle Art") , ("Pen Drawings","Pen Drawings") , ("Nature Arts","Nature Arts") )
    category=models.CharField(max_length=100, blank=False,choices=category_choice)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    caption = models.CharField(max_length=200,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    price = models.DecimalField(max_digits=1000, decimal_places=0)

    class Meta:
        db_table = "post_table"
    def __str__(self):
        return self.art_name

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




# Create your models here.
class Admin(models.Model):
    username=models.CharField(primary_key=True,max_length=100,blank=False,unique=True)
    email=models.CharField(max_length=100,blank=False,unique=True)
    password=models.CharField(max_length=100,blank=False)

    class Meta:
        db_table = "admin_table"

    def __str__(self):
        return self.username


class User(models.Model):
    FullName=models.CharField(max_length=100,blank=False)
    DateOfBirth=models.DateField(blank=False)
    Gender_choices = (("Male", "M"), ("Female", "F"), ("Other", "O"))
    Gender=models.CharField(max_length=10,blank=False,choices=Gender_choices)
    Username=models.CharField(max_length=100,blank=False,primary_key=True,unique=True)
    MobileNumber = models.CharField(max_length=10, blank=False, unique=True)
    Email = models.CharField(max_length=100, blank=False, unique=True)
    password = models.CharField(max_length=100, blank=False )


    class Meta:
        db_table = "user_table"

    def __str__(self):
        return self.Username


class Profile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=False, primary_key=True, unique=True,default='user2086')
    user_pic = models.ImageField(upload_to='user_pics/', default='static/user_profiles/userpic.png')

    bio = models.TextField(default='Add Bio✏️')

    class Meta:
        db_table = "profile_table"

    def __str__(self):
        return str(self.user)

class CartItem(models.Model):
    art_name = models.CharField(max_length=100, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # If your cart is user-specific
    product = models.ForeignKey(Post, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=1000, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='posts/',default='static/user_profiles/userpic.png')

    class Meta:
        db_table = "cart_table"