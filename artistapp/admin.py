from django.contrib import admin
from .models import Artist,Post,ArtistProfile,Admin,User,Profile,CartItem

admin.site.register(Artist)
admin.site.register(ArtistProfile)
admin.site.register(Post)
# Register your models here.

admin.site.register(Admin)
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(CartItem)