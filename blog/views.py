from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from .models import Post, Tag
from .forms import PostForm
from .services import generate_blog_post

def home(request):
    posts = Post.objects.filter(published=True).order_by('-created_at')
    tag = request.GET.get('tag')
    if tag:
        posts = posts.filter(tags__name=tag)
    all_tags = Tag.objects.all()
    return render(request, 'blog/home.html', {
        'posts': posts,
        'tag': tag,
        'all_tags': all_tags
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    return render(request, 'blog/post_detail.html', {'post': post})

"""
If a logged-out user visits /post/create/, Django automatically redirects them to the login page. 
This decorator is one of the most used in Django — you'll put it on any view that requires authentication.
"""
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # don't save to DB yet
            post.author = request.user      # attach the logged-in user
            post.save()
            form.save_m2m()                 # save ManyToMany fields (tags)
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})
"""
Three things to understand:

commit=False — creates the Python object but doesn't hit the database yet. 
Gives you a chance to add extra data (like author) before saving.
form.save_m2m() — required when you use commit=False with a form that has ManyToMany fields. 
Django can't save the tag relationships until the post has an ID.
redirect() — sends the user to a different URL after a successful save. 
Always redirect after a successful form submission — this prevents duplicate submissions if the user refreshes the page.

"""

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)  # ← instance is the key difference
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.save_m2m()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)  # ← pre-fills the form with existing data
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def generate_post(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        generated = generate_blog_post(topic)
        post = Post.objects.create(
            title=generated['title'],
            content=generated['content'],
            slug=slugify(generated['title']),
            author=request.user,
            published=False
        )
        return redirect(post.get_absolute_url())
    return render(request, 'blog/generate.html')

"""
This is the api pattern for forms
if request.method == 'POST':
    # form was submitted — validate and save
else:
    # page was opened — show empty form
"""