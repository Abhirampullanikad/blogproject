from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import *
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage

from .models import Comment, Post
from django.contrib.auth import get_user_model
from Account.models import Profile
User = get_user_model()
from .forms import NewsForm


# Create your views here.
def index(request):
    return render(request, "index.html", {
        'posts': Post.objects.filter(user_id=request.user.id).order_by("id").reverse(),
        'top_posts': Post.objects.all().order_by("-likes"),
        'recent_posts': Post.objects.all().order_by("-id"),
        'user': request.user,
        'media_url': settings.MEDIA_URL,
        'newses': News.objects.all().order_by('-time')         
    
    })

def blog(request):
    return render(request, "blog.html", {
        'posts': Post.objects.filter(user_id=request.user.id).order_by("id").reverse(),
        'top_posts': Post.objects.all().order_by("-likes"),
        'recent_posts': Post.objects.all().order_by("-id"),
        'user': request.user,
        'media_url': settings.MEDIA_URL
    })


def create(request):
    if request.method == 'POST':
        try:
            postname = request.POST['postname']
            content = request.POST['content']
            category = request.POST['category']
            image = request.FILES['image']
            Post(postname=postname, content=content, category=category, image=image, user=request.user).save()
        except:
            print("Error")
        return redirect('blogapp:index')
    else:
        return render(request, "create.html")





def profileedit(request, id):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']


        user = User.objects.get(id=id)
        user.first_name = firstname
        user.email = email
        user.last_name = lastname
        user.save()
        return profile(request, id)
    return render(request, "profileedit.html", {
        'user': User.objects.get(id=id),
    })


def increaselikes(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        post.likes += 1

        post.save()
    return redirect("blogapp:index")


def post(request, id):
    post = Post.objects.get(id=id)

    return render(request, "post-details.html", {
        "user": request.user,
        'post': Post.objects.get(id=id),
        'recent_posts': Post.objects.all().order_by("-id"),
        'media_url': settings.MEDIA_URL,
        'comments': Comment.objects.filter(post_id=post.id),
        'total_comments': len(Comment.objects.filter(post_id=post.id))
    })


def savecomment(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        content = request.POST['message']
        Comment(post_id=post.id, user_id=request.user.id, content=content).save()
        return redirect("blogapp:index")


def deletecomment(request, id):
    comment = Comment.objects.get(id=id)
    postid = comment.post.id
    comment.delete()
    return post(request, postid)


def editpost(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        try:
            postname = request.POST['postname']
            content = request.POST['content']
            category = request.POST['category']

            post.postname = postname
            post.content = content
            post.category = category
            post.save()
        except:
            print("Error")
        return profile(request, request.user.id)

    return render(request, "postedit.html", {
        'post': post
    })


def deletepost(request, id):
    Post.objects.get(id=id).delete()
    return profile(request, request.user.id)





def listblog(request):
    posts=Post.objects.all()

    paginator=Paginator(posts,4)
    page_number=request.GET.get('page')
    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_pages)

    return render(request,'user/listpost.html',{'posts':posts,'page':page})

def detailsview(request,id):
    Post.objects.get(id=id)
    return render(request,'user/detailsview.html',{'post':post})

def deleteview(request,id):
    post=Post.objects.get(id=id)
    if request.method=='POST':
        post.delete()

        return redirect('blogapp:listpost')

    return render(request,'user/deleteview.html',{'post':post})



def search_post(request):
    query = None
    books = None

    if 'q' in request.GET:
        query = request.GET.get('q')
        posts = Post.objects.filter(Q(title__icontains=query))

    else:
        posts = []

    return render(request, 'search.html', {'posts': posts, 'query': query})



def base(request):
    return render(request,'user/base.html')


def listpost(request):
    books = Post.objects.all()

    paginator = Paginator(books, 4)
    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(page_number.num_pages)

    return render(request, 'user/listpost.html', {'books': books, 'page': page})


def profile(request, id):
    user = get_object_or_404(User, id=id)

    # Get or create profile if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=user)

    context = {
        'user_profile': user,
        'profile': profile,
        'user': request.user,
        
    }
    return render(request, 'profile.html', context)


def CreateNews(request):
    
    newses=News.objects.all()
    
    if request.method=='POST':
        form=NewsForm(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
        return redirect('blogapp:listnews')
    else:
            form=NewsForm()
    return render(request,'news.html',{'form':form,'newses': newses})  


def listNews(request):
 
    newses=News.objects.all()
    
    paginator=Paginator(newses,4)
    page_number=request.GET.get('page')
    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_pages)
        
    
    return render(request,'listnews.html',{'newses':newses,'page':page})



def updateNews(request, news_id):
    news = get_object_or_404(News, id=news_id)

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('blogapp:listnews')
    else:
        form = NewsForm(instance=news)

    return render(request, 'updateview.html', {'form': form})


def DeleteView(request,news_id):
    
    news=News.objects.get(id=news_id)
    
    if request.method=='POST':
        
        news.delete()
        
        return redirect('blogapp:listnews')
    
    return render(request,'deletenews.html',{'news':news})





