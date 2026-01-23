from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import SupportCircle, CirclePost, CircleComment, CircleLike
from .forms import SupportCircleForm, CirclePostForm, CircleCommentForm

class CircleListView(ListView):
    """Display all support circles"""
    model = SupportCircle
    template_name = 'Support_Circle/circle_list.html'
    context_object_name = 'circles'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = SupportCircle.objects.all()
        focus = self.request.GET.get('focus')
        if focus:
            queryset = queryset.filter(focus_area=focus)
        return queryset

class CircleDetailView(DetailView):
    """Display a specific support circle and its posts"""
    model = SupportCircle
    template_name = 'Support_Circle/circle_detail.html'
    context_object_name = 'circle'

@login_required
def create_circle(request):
    """Create a new support circle"""
    if request.method == 'POST':
        form = SupportCircleForm(request.POST)
        if form.is_valid():
            circle = form.save(commit=False)
            circle.creator = request.user
            circle.save()
            circle.members.add(request.user)
            messages.success(request, 'Support circle created!')
            return redirect('Support_Circle:circle_detail', pk=circle.pk)
    else:
        form = SupportCircleForm()
    
    return render(request, 'Support_Circle/create_circle.html', {'form': form})

@login_required
def join_circle(request, pk):
    """Join a support circle"""
    circle = get_object_or_404(SupportCircle, pk=pk)
    
    if request.user in circle.members.all():
        messages.info(request, 'You are already a member of this circle!')
    else:
        circle.members.add(request.user)
        messages.success(request, f'You joined {circle.name}!')
    
    return redirect('Support_Circle:circle_detail', pk=pk)

@login_required
def leave_circle(request, pk):
    """Leave a support circle"""
    circle = get_object_or_404(SupportCircle, pk=pk)
    
    if request.user == circle.creator:
        messages.error(request, 'Circle creators cannot leave their circle!')
    else:
        circle.members.remove(request.user)
        messages.success(request, f'You left {circle.name}!')
    
    return redirect('Support_Circle:circle_list')

@login_required
def edit_circle(request, pk):
    """Edit a support circle"""
    circle = get_object_or_404(SupportCircle, pk=pk)
    
    if request.user != circle.creator:
        messages.error(request, 'Only the creator can edit this circle!')
        return redirect('Support_Circle:circle_detail', pk=pk)
    
    if request.method == 'POST':
        form = SupportCircleForm(request.POST, instance=circle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Circle updated!')
            return redirect('Support_Circle:circle_detail', pk=pk)
    else:
        form = SupportCircleForm(instance=circle)
    
    return render(request, 'Support_Circle/edit_circle.html', {'form': form, 'circle': circle})

@login_required
def delete_circle(request, pk):
    """Delete a support circle"""
    circle = get_object_or_404(SupportCircle, pk=pk)
    
    if request.user != circle.creator:
        messages.error(request, 'Only the creator can delete this circle!')
        return redirect('Support_Circle:circle_detail', pk=pk)
    
    if request.method == 'POST':
        circle_name = circle.name
        circle.delete()
        messages.success(request, f'Circle "{circle_name}" deleted!')
        return redirect('Support_Circle:circle_list')
    
    return render(request, 'Support_Circle:circle_detail', pk=pk)

@login_required
def my_circles(request):
    """View circles user is part of"""
    circles = request.user.support_circles.all()
    return render(request, 'Support_Circle/my_circles.html', {'circles': circles})

@login_required
def create_post(request, circle_id):
    """Create a post in a support circle"""
    circle = get_object_or_404(SupportCircle, id=circle_id)
    
    if request.user not in circle.members.all():
        messages.error(request, 'You must be a member to post!')
        return redirect('Support_Circle:circle_list')
    
    if request.method == 'POST':
        form = CirclePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.circle = circle
            post.author = request.user
            post.save()
            messages.success(request, 'Post created!')
            return redirect('Support_Circle:circle_detail', pk=circle.id)
    else:
        form = CirclePostForm()
    
    return render(request, 'Support_Circle/create_post.html', {'form': form, 'circle': circle})

@login_required
def add_comment(request, post_id):
    """Add a comment to a post"""
    post = get_object_or_404(CirclePost, id=post_id)
    
    if request.user not in post.circle.members.all():
        messages.error(request, 'You must be a member to comment!')
        return redirect('Support_Circle:circle_list')
    
    if request.method == 'POST':
        form = CircleCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')
    
    return redirect('Support_Circle:circle_detail', pk=post.circle.id)

@login_required
def like_post(request, post_id):
    """Like a circle post"""
    post = get_object_or_404(CirclePost, id=post_id)
    
    like, created = CircleLike.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        like.delete()
        messages.info(request, 'Like removed!')
    else:
        messages.success(request, 'Post liked!')
    
    return redirect('Support_Circle:circle_detail', pk=post.circle.id)

