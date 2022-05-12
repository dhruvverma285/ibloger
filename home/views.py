from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from home.models import Contact
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
def sendmail(email):
    try:
        from mailjet_rest import Client
        api_key = '56d6031e36028ba2a81a23420edbf608'
        api_secret = '59f25017cd36a762ab02b226deb20690'
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
        'Messages': [
                        {
                                "From": {
                                        "Email": "myfreeid13@gmail.com",
                                        "Name": "Me"
                                },
                                "To": [
                                        {
                                                "Email": email,
                                                "Name": "You"
                                        }
                                ],
                                "Subject": "Order Place",
                                "TextPart": "Greetings from Mailjet!",
                                "HTMLPart": f"Your Otp is : 123456"
                        }
                ]
        }
        mailjet.send.create(data=data)
    except Exception as e:
        return HttpResponse("Eroor")

#html page
def index(request):
    allpost = len(Post.objects.all())
    post = []
    post.append(Post.objects.filter(pno=allpost)[0])
    for i in range(1,3):
        post.append(Post.objects.filter(pno=(allpost-i))[0])
    context = {'allpost':post}
    return render(request ,'home/home.html',context)

def contact(request):
    
    if request.method=='POST':
        name = str(request.POST.get('name', '')).capitalize()
        phone = request.POST.get('phone', '')
        email = str(request.POST.get('email', '')).capitalize()
        query = str(request.POST.get('query', '')).lower()
        if len(name)<3 or len(phone)<4 or len(email)<4 or len(query)<4:
            print("Not Prpper")
            messages.error(request,"Fill correctly")
        else:
            contact = Contact(name=name, phone=phone, email=email, Query=query)
            contact.save()
            messages.success(request,"Your query is submit.")
            print("Working")
    return render(request ,'home/contact.html')

def about(request):
    return render(request ,'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query)==0:
        messages.error(request,"Please write something")
        return render(request,'home/search.html')

    if len(query)>80:
        allpost = []
    else:
      allpost = Post.objects.filter(title__icontains=query)
    if len(allpost)!=0:
        context = {'allpost':allpost}
        return render(request,'home/search.html',context)
    else:
        return render(request,'home/search.html',{'error':True})


#Auth APIs
def signuphandel(request):
    if request.method=='POST':
        username = str(request.POST['username']).lower()
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # CHeck for error input
        if len(username)>10 :
            messages.error(request,"User must be under 10 characters")
            return redirect('home')

        if len(fname)==0 or len(email)==0 or len(pass1)<8 or len(pass2)<8:
            messages.error(request,"Fill correctly")
            return redirect('home')
        
        if  pass1 != pass2:
            messages.error(request,"Enter Same password")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request,"Username should contain only letter and numbers")
            return redirect('home')
        

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        user = authenticate(username=username,password=pass1)
        login(request,user)
        messages.success(request,"Successfully signup")
        return redirect('home')
    else:
        return HttpResponse('404 error')

def loginhandel(request):
    if request.method=='POST':
        loginusername = str(request.POST['loginusername']).lower()
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername,password=loginpassword)

        print(user)

        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged in")
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials,Please try again")
            return redirect('home')
    else:
        return HttpResponse("404 Error")

@login_required
def logouthandel(request):
    logout(request)
    messages.success(request,'Successfully Logged Out')
    return redirect('home')