from django.contrib import admin

# Register your models here.
from blog.models import Post,Blogcomment
admin.site.register((Post,Blogcomment))