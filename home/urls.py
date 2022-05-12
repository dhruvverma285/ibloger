from django.urls import path
from home import views

urlpatterns = [
    path('',views.index,name='home'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('search/',views.search,name='search'),
    path('signup/',views.signuphandel,name='signuphandel'),
    path('login/',views.loginhandel,name='loginhandel'),
    path('logout/',views.logouthandel,name='logouthandel'),
    
]
