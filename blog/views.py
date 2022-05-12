from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from blog.models import Post, Blogcomment
from django.contrib.auth.decorators import login_required
# Create your views here.


def bloghome(request):
    allpost = Post.objects.all()
    context = {'allpost': allpost}
    return render(request, 'blog/index.html', context)


def blogpost(request, slug):
    try:
        post = Post.objects.filter(pno=int(slug)).first()
        post.views = post.views + 1
        post.save()
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        print(ip)
        if post is None:
            allpost = len(Post.objects.all())
            req = str(request.build_absolute_uri()).split('/')[::-1][0]
            c = req.isdigit()
            if c == True:
                if req == '0':
                    req = '1'
                else:
                    req = str((int(req)-1))
                    if int(req) > allpost:
                        return HttpResponse("404 Page not found")

                messages.error(request, "Post are not Found or Error")
                return redirect(f'/blog/{req}')
            else:
                messages.error(request, "Post are not Found or Error")
                return redirect('/blog')
        comment = Blogcomment.objects.filter(post=post, parent=None)
        replys = Blogcomment.objects.filter(post=post).exclude(parent=None)
        replydict = dict({})
        for reply in replys:
            if reply.parent.sno not in replydict.keys():
                replydict[reply.parent.sno] = [reply]

            else:
                replydict[reply.parent.sno].append(reply)

        context = {'post': post, 'old': int(slug)-1, 'new': int(
            slug)+1, 'comments': comment, 'count': len(comment), "replydict": replydict}
        return render(request, 'blog/blogpost.html', context)

    except Exception as e:
        print(e)
        messages.error(request, "Post are not Found or Error")
        return redirect('/blog')


@login_required
def postcomment(request):
    if request.method == 'POST':
        comment = str(request.POST['comment'])
        user =      request.user
        postid =    request.POST['postid']
        parentsno = request.POST['parentsno']
        post =      Post.objects.filter(pno=int(postid))[0]

        if len(comment) < 4 :
            messages.success(request, "Please Enter valid messase or reply")
            return redirect(f"/blog/{post.pno}")                

        if parentsno == "":
            comment = Blogcomment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(
                request, "your Reply has been posted successfully")
        else:
            parent = Blogcomment.objects.get(sno=parentsno)
            comment = Blogcomment(
                comment=comment, user=user, post=post, parent=parent)
            messages.success(
                request, "your Reply has been posted successfully")
            comment.save()

        return redirect(f"/blog/{post.pno}")

