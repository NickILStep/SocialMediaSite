from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import CreatePostForm, CreateCommentForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from user.models import Profile, User

# Create your views here.
def index(request):
    return render(request, 'feed/index.html', {})

@login_required
def feed(request):
    post_list = Post.objects.all().order_by('-datetime')

    post_search = request.GET.get('post_content')
    if post_search != '' and post_search is not None:
        post_list = post_list.filter(Q(title__icontains=post_search) | Q(content__icontains=post_search))
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    post_list = paginator.get_page(page)

    return render(request, 'feed/feed.html', {'post_list': post_list})

@login_required
def postDetail(request, post_id):
    post = Post.objects.get(pk=post_id)
    comment_list = Comment.objects.filter(post=post, parent__isnull=True).order_by('-id')
    return render(request, 'feed/postDetail.html', {'post': post, 'comment_list': comment_list})

@login_required
def createPost(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'feed/feed.html', {})
    else:
        form = CreatePostForm()

    return render(request, 'feed/createPost.html', {'form': form})

class CreatePost(CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'feed/createPost.html'
    success_url = reverse_lazy('feed:feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def updatePost(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CreatePostForm(request.POST or None, request.FILES or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect(request.GET.get('next'))

    return render(request, 'feed/createPost.html', {'form': form, 'post': post})

@login_required
def deletePost(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        post.delete()
        return redirect('feed:feed')

    return render(request, 'feed/deletePost.html', {'post': post})

@login_required
def commentDetail(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment_list = Comment.objects.filter(parent=comment).order_by('-id')

    return render(request, 'feed/commentDetail.html', {'comment': comment, 'comment_list': comment_list})

@login_required
def createComment(request):
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'feed/feed.html', {})
    else:
        form = CreateCommentForm()

    return render(request, 'feed/createComment.html', {'form': form})

class CreateComment(CreateView):
    model = Comment
    fields = ['title', 'content']
    template_name = 'feed/createComment.html'
    success_url = reverse_lazy('feed:feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(id=int(self.request.GET.get('post_id')))
        if self.request.GET.get('comment_id'):
            form.instance.parent = Comment.objects.get(id=int(self.request.GET.get('comment_id')))
        return super().form_valid(form)

@login_required
def updateComment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    form = CreateCommentForm(request.POST or None, instance=comment)

    if form.is_valid():
        form.save()
        return redirect(request.GET.get('next'))

    return render(request, 'feed/createComment.html', {'form': form, 'comment': comment})

@login_required
def deleteComment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)

    if request.method == 'POST':
        comment.delete()
        return redirect(request.GET.get('next'))

    return render(request, 'feed/deleteComment.html', {'comment': comment})

@login_required
def savePost(request, post_id):
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        profile.savedPosts.add(post)
        return redirect(request.GET.get('next'))

    return render(request, 'feed/savePost.html', {'post': post, 'profile': profile})

@login_required
def unsavePost(request, post_id):
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        profile.savedPosts.remove(post)
        return redirect(request.GET.get('next'))

    return render(request, 'feed/unsavePost.html', {'post': post, 'profile': profile})

@login_required
def likePost(request, post_id):
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        post.likes.add(profile)
        profile.likedPosts.add(post)
        return redirect(request.GET.get('next'))

    return render(request, 'feed/likePost.html', {'post': post, 'profile': profile})

@login_required
def unlikePost(request, post_id):
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        post.likes.remove(profile)
        profile.likedPosts.remove(post)
        return redirect(request.GET.get('next'))

    return render(request, 'feed/unlikePost.html', {'post': post, 'profile': profile})