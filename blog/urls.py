from django.urls import path
from blog import views

urlpatterns = [
    path('postcomment/',views.postcomment,name='postcomment'),
    path('',views.bloghome,name='bloghome'),
    path('<str:slug>',views.blogpost,name='blogpost'),

]
