from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path("home",views.homefunction,name="home"),

path("cart",views.cartfun,name="cart"),
    path("checkartistlogin", views.checkartistlogin, name="checkartistlogin"),
path('create_post/artlogin1', views.artlogin1, name='artlogin1'),

    path("dartsp", views.dartsp, name="dartsp"),

    path('artistprofilefun/', views.artistprofilefun, name='artistprofilefun'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path("checkuserlogin",views.checkuserlogin,name="checkuserlogin"),


    path("dusersp",views.dusersp,name="dusersp"),

    path("login1fun",views.login1fun,name="login1fun"),
    path('search/', views.search, name='search'),

    path("viewuser",views.viewuser,name="viewuser"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),


    path('add_to_cart/<str:art_name>/<str:image>/<int:price>/', views.add_to_cart, name='add_to_cart'),

    path("checkout",views.checkout,name="checkout"),
    path("transSuccess",views.transSuccess,name="transSuccess"),
    path("aesth",views.aesth,name="aesth"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
