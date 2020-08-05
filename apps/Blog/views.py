from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import User, Post
import bcrypt

def WelcomePage (request):
    users = User.objects.all()
    posts = Post.objects.all()

    # for user in users:
    #     user.delete()
    # for post in posts:
    #     post.delete()
    print('session.first_name' in request)
    return render (request, 'home.html')

def user_register (request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User(
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
                email = request.POST.get('email'),
                password = request.POST.get('password').encode(),
            )
            user.save()
    request.session['first_name'] = user.first_name
    request.session['user_email'] = user.email
    return redirect('/')

def user_signin (request):
    try:
        errors = User.objects.login_validator(request.POST)
        if len(errors) < 1:
            user = User.objects.filter(email=request.POST.get('login_email'))[0]
            request.session['first_name'] = user.first_name
            request.session['user_email'] = user.email
            return redirect('/homepage')
        else:
            messages.error(request, 'Password Is Not Valid')
            return redirect ('/')

    except ValueError:
        messages.error(request, 'User Not Found')
        return redirect ('/')

def login (request):
    return render (request, 'login.html')

def profile (request):
    user = None
    try:
        user = User.objects.filter(email=request.session['user_email'])[0]
    except KeyError:
        return redirect('/login')
    
    context = {'user': user}
    return render (request, 'profile.html', context)

def register (request):
    return render (request, 'register.html')

def logout (request):
    try:
        del request.session['first_name']
        del request.session['user_email']
    except KeyError:
        pass
    return render (request, 'logout.html')

def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('/homepage')

def submit(request):
    if request.method == 'POST':
        errors = Post.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/post/new')
        else:
            posts = Post(
                post=request.POST.get('Post'),
                end_date=request.POST.get('end_date'),
                plan=request.POST.get('plan'),
            )
            posts.save()
        return redirect('/homepage')


def allposts(request):
    allposts = Post.objects.all()
    first_name = request.session['first_name']
    context = {'dashboard': Post, 'first_name': first_name}
    return render(request, 'homepage.html', context)


def newpost(request):
    user = None
    try:
        user = User.objects.filter(email=request.session['user_email'])[0]
    except KeyError:
        return redirect('/login')
    return render(request, 'post_form.html')

def postdetail(request, post_id):
    first_name = request.session['first_name']
    context = {'single_post': Post.objects.get(pk=post_id), 'first_name': first_name}
    return render(request, 'post_detail.html', context)

def editpost(request, post_id):
    if request.method == 'GET':
        context = {'post': Post.objects.get(pk=post_id)}
        return render(request, 'edit_post.html', context)
    if request.method == 'POST':
        errors = Post.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/post/edit/'+ str(post_id))
        else:
            post_update = Post.objects.get(pk=post_id)
            post_update.post_content=request.POST.get('post_content')
            post_update.save()
            return redirect('/homepage')


# Create your views here.
