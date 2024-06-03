from django.shortcuts import render, redirect
from .forms import RegistrationForm, UpdateProfileForm
from .models import User, Profile
from feed.models import Post
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('user:login')
    else:
        form = RegistrationForm()
    return render(request, 'user/register.html', {'form': form})

@login_required
def profilepage(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    post_list = Post.objects.filter(user=user).order_by('-id')

    post_search = request.GET.get('post_content')
    if post_search != '' and post_search is not None:
        post_list = post_list.filter(Q(title__icontains=post_search) | Q(content__icontains=post_search))

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    post_list = paginator.get_page(page)

    title = "Posts:"
    mode = 'profile'

    return render(request, 'user/profile.html', {'profile': profile, 'post_list': post_list, 'title': title, 'mode': mode})

@login_required
def savedPosts(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    post_list = profile.savedPosts.all().order_by('-id')

    post_search = request.GET.get('post_content')
    if post_search != '' and post_search is not None:
        post_list = post_list.filter(Q(title__icontains=post_search) | Q(content__icontains=post_search))

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    post_list = paginator.get_page(page)

    title = "Saved Posts:"
    mode = 'savedPosts'

    return render(request, 'user/profile.html', {'profile': profile, 'post_list': post_list, 'title': title, 'mode': mode})

@login_required
def likedPosts(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    post_list = profile.likedPosts.all().order_by('-id')

    post_search = request.GET.get('post_content')
    if post_search != '' and post_search is not None:
        post_list = post_list.filter(Q(title__icontains=post_search) | Q(content__icontains=post_search))

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    post_list = paginator.get_page(page)

    title = "Liked Posts:"
    mode = 'likedPosts'

    return render(request, 'user/profile.html', {'profile': profile, 'post_list': post_list, 'title': title, 'mode': mode})

@login_required
def followingPosts(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    following_list = profile.following.all()

    post_id_list = set()
    for following in following_list:
        for post in Post.objects.filter(user=following.user):
            post_id_list.add(post.id)

    post_list = Post.objects.filter(pk__in=post_id_list).order_by('-id')

    post_search = request.GET.get('post_content')
    if post_search != '' and post_search is not None:
        post_list = post_list.filter(Q(title__icontains=post_search) | Q(content__icontains=post_search))

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    post_list = paginator.get_page(page)

    title = "Followed Accounts' Posts:"
    mode = 'followingPosts'

    return render(request, 'user/profile.html', {'profile': profile, 'post_list': post_list, 'title': title, 'mode': mode})

@login_required
def followers(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    follower_list = profile.followers.all()

    return render(request, 'user/followers.html', {'profile': profile, 'follower_list': follower_list})

@login_required
def editProfile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if form.is_valid():
        form.save()
        return redirect(request.GET.get('next'))

    return render(request, 'user/editProfile.html', {'form': form, 'profile': profile})

class UpdateProfile(UpdateView):
    model = Profile
    fields = ['bio', 'image']
    template_name = 'user/editProfile.html'
    success_url = reverse_lazy('feed:feed')

@login_required
def followProfile(request, profile_id):
    profileToFollow = Profile.objects.get(id=profile_id)
    profileFollowing = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        profileFollowing.following.add(profileToFollow)
        profileToFollow.followers.add(profileFollowing)
        return redirect(request.GET.get('next'))

    return render(request, 'user/followProfile.html', {'profileToFollow': profileToFollow, 'profileFollowing': profileFollowing})

@login_required
def unfollowProfile(request, profile_id):
    profileToFollow = Profile.objects.get(id=profile_id)
    profileFollowing = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        profileFollowing.following.remove(profileToFollow)
        profileToFollow.followers.remove(profileFollowing)
        return redirect(request.GET.get('next'))

    return render(request, 'user/unfollowProfile.html', {'profileToFollow': profileToFollow, 'profileFollowing': profileFollowing})

@login_required
def deleteUser(request, username):
    user = User.objects.get(username=username)

    if request.method == 'POST':
        user.delete()
        return redirect('feed:index')

    return render(request, 'user/deleteUser.html', {'user': user})

