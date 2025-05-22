from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.conf import settings

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf

from .models import Post,Artist,ArtistProfile,User,Profile,Admin,CartItem
from .forms import PostForm, CommentForm, UserProfileEditForm, AddToCartForm


def demofunction(request):
    return HttpResponse("<font color='red' >Redirect to Home Page</font>")


def homefunction(request):
    return render(request, "index.html")
def artlogin1(request):
    return render(request, 'artlogin1.html')
def checkartistlogin(request):
    if request.method == "POST":
        artistuname=request.POST["artist_username"]
        artistpwd=request.POST["artist_password"]

        artt = Artist.objects.filter(Q(Username=artistuname) & Q(password=artistpwd)).first()
        arts = Post.objects.all()

        if artt:
            apic=artt.artistprofile.artist_pic
            abio=artt.artistprofile.bio
            sm=artt.artistprofile.social_media
            ausername = artt.Username

            return render(request, "artlogin1.html", {"ausername": ausername,"arts":arts,"apic":apic,"abio":abio,"sm":sm}, )
        else:
            return render(request, "Nartlogin.html")


    return render(request, "artlogin.html")

def dartsp(request):

    if request.method=="POST":
        fn=request.POST["FullName"]
        dob= request.POST["DOB"]
        mn=request.POST["MobileNumber"]
        gn=request.POST["gender"]
        un=request.POST["username"]
        em=request.POST["email"]
        pw=request.POST["password"]
        toa=request.POST["type"]

        art = Artist(FullName=fn,DateOfBirth=dob,MobileNumber=mn,Gender=gn,Username=un,Email=em,password=pw,TypeOfArtist=toa)

        Artist.save(art)

        return render(request,"posts/artistprofile.html")


@login_required
def artistprofilefun(request):
    user = request.user

    try:
        artist = ArtistProfile.objects.get(artist=user)

    except ArtistProfile.DoesNotExist:
        # Handle the case where an ArtistProfile doesn't exist for the user
        artist = None

    posts = Post.objects.filter(user=user)
    return render(request, 'posts/artistprofile.html', {'artist': artist, 'posts': posts})


def addart(request):
    if not request.user.is_authenticated :
        return redirect('artlogin1')
    a={}
    a.update(csrf(request))
    username=request.user.username
    if username=='KOWSIK2004' :
        return render(request,'addart.html',a)
    else :
        return redirect('index')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return render(request,'artlogin1.html')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = post.comment_set.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


def checkuserlogin(request):
    if request.method == "POST":
        useruname = request.POST["user_username"]
        userpwd = request.POST["user_password"]

        # Check if a user with the provided username and password exists
        user = User.objects.filter(Q(Username=useruname) & Q(password=userpwd)).first()
        arts = Post.objects.all()
        if user:
            # If a user is found, you can access their username and profile picture
            username = user.Username
            bio=user.profile.bio
            pic=user.profile.user_pic

            return render(request, "login1.html", {"username": username, "bio" : bio, "pic" : pic,"arts":arts},)
        else:
            return render(request, "Nuserlogin.html")

    return render(request, "userlogin.html")



def dusersp(request):

    if request.method=="POST":
        fnm=request.POST["FullName"]
        dobs= request.POST["DOB"]
        mns=request.POST["MobileNumber"]
        gns=request.POST["gender"]
        uns=request.POST["username"]
        ems=request.POST["email"]
        pws=request.POST["password"]

        us = User(FullName=fnm,DateOfBirth=dobs,MobileNumber=mns,Gender=gns,Username=uns,Email=ems,password=pws)

        User.save(us)

        return render(request,"login1.html")

def your_view(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        secret_key = settings.RECAPTCHA_SECRET_KEY

        data = {
            'secret': secret_key,
            'response': recaptcha_response,
        }

        response = request.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()

        if result['success']:
            # CAPTCHA verification passed; process the form data
            # Your form processing logic here
            return redirect('login1.html')
        else:
            # CAPTCHA verification failed; show an error message
            return render(request, 'artsp.html', {'error_message': 'CAPTCHA verification failed'})

    return render(request, 'artsp.html')

def viewuser(request):
    user=User.objects.all()
    return render(request,{"userdata":user})

# Profile view

def login1fun(request):
    return render(request,'login1.html')


from django.contrib.auth.decorators import login_required

@login_required

# Your view function for editing the profile
def edit_profile(request):
    user = request.user  # Get the currently logged-in user

    if request.method == 'POST':

        form = UserProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():

            form.save()

            # Redirect to a success page or wherever needed
            return redirect('login1fun')  # Change 'login1fun' to your actual URL name

    else:
        form = UserProfileEditForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})


def add_to_cart(request, art_name, image, price):

    # Get the selected post based on its art_name or return a 404 if not found
    post = get_object_or_404(Post, art_name=art_name,image=image,price=price)

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(post=post, user=request.user)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('artlogin1')

def cartfun(request):

    return render(request,"cart.html",)

def search(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    results = Post.objects.filter(art_name__icontains=query)  # Filter the arts based on the query

    return render(request, 'search_results.html', {'results': results, 'query': query})


def checkout(request):
    return render(request,"checkout.html")

def transSuccess(request):
    return render(request,"tran_succ.html")

def aesth(request):
    arts = Post.objects.all()
    return render(request,"aesth.html",{'arts':arts})

