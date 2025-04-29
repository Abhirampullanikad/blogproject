from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from .models import CustomUser
from blogapp.models import Post
from .models import Profile
# Custom User model would be defined in models.py as shown previously
User = CustomUser


def userRegistration(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        password1 = request.POST.get('password1', '').strip()
        profile_pic = request.FILES.get('profile_pic')
        first_name=request.POST.get('first_name','').strip()
        last_name=request.POST.get('last_name','').strip()
        

        # Validate inputs
        if not all([username, email, password, password1]):
            messages.error(request, 'All fields are required!')
            return redirect('Account:register')

        if password != password1:
            messages.error(request, 'Passwords do not match!')
            return redirect('Account:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('Account:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('Account:register')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                profile_pic=profile_pic,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, 'Registration successful! Please login.')
            return redirect('Account:login')
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('Account:register')

    return render(request, 'user/register.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser or user.user_type == 'admin':
                return redirect('Account:admin_view')
            return redirect('Account:user_view')
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'user/login.html')


@login_required
def admin_view(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, 'user/base.html', {
        'posts': posts,
        'user': request.user
    })


@login_required
def user_view(request):
    user_posts = Post.objects.filter(user=request.user).order_by('-id')
    return render(request, 'profile.html', {
        'user': request.user,
        'posts': user_posts,
        'is_authenticated': True
    })






def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('Account:login')


def search_post(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    else:
        posts = []
    return render(request, 'search.html', {
        'posts': posts,
        'query': query,
        'user': request.user if request.user.is_authenticated else None
    })


@login_required
def profile_edit(request, id):
    # Ensure users can only edit their own profile
    if request.user.id != id:
        messages.error(request, "You can only edit your own profile!")
        return redirect('profile', id=request.user.id)

    user = get_object_or_404(User, id=id)
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        # Update user fields
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)

        # Update profile picture if exists in CustomUser
        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']

        # Update profile fields
        profile.bio = request.POST.get('bio', profile.bio)
        profile.website = request.POST.get('website', profile.website)
        profile.location = request.POST.get('location', profile.location)

        user.save()
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile', id=user.id)

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'user/profile_edit.html', context)