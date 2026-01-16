from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.models import User
from .models import HormonalTwin, TwinConnection
from .forms import HormonalTwinProfileForm, TwinConnectionForm

class TwinListView(ListView):
    """Display all hormonal twins"""
    model = HormonalTwin
    template_name = 'Hormonal_Twins/twin_list.html'
    context_object_name = 'twins'
    paginate_by = 12

class TwinDetailView(DetailView):
    """Display a specific hormonal twin's profile"""
    model = HormonalTwin
    template_name = 'Hormonal_Twins/twin_detail.html'
    context_object_name = 'twin'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'

@login_required
def create_twin_profile(request):
    """Create or update hormonal twin profile"""
    try:
        twin = request.user.hormonal_twin_profile
        is_new = False
    except HormonalTwin.DoesNotExist:
        twin = None
        is_new = True
    
    if request.method == 'POST':
        form = HormonalTwinProfileForm(request.POST, request.FILES, instance=twin)
        if form.is_valid():
            twin = form.save(commit=False)
            twin.user = request.user
            twin.save()
            messages.success(request, 'Profile saved successfully!')
            return redirect('Hormonal_Twins:my_profile')
    else:
        form = HormonalTwinProfileForm(instance=twin)
    
    return render(request, 'Hormonal_Twins/create_profile.html', {'form': form, 'is_new': is_new})

@login_required
def my_profile(request):
    """View current user's hormonal twin profile"""
    try:
        twin = request.user.hormonal_twin_profile
        matches = twin.get_matches()
    except HormonalTwin.DoesNotExist:
        twin = None
        matches = []
    
    return render(request, 'Hormonal_Twins/my_profile.html', {
        'twin': twin,
        'matches': matches,
    })

@login_required
def find_matches(request):
    """Find hormonal twin matches"""
    try:
        user_twin = request.user.hormonal_twin_profile
    except HormonalTwin.DoesNotExist:
        messages.error(request, 'Please create your profile first!')
        return redirect('Hormonal_Twins:create_profile')
    
    issue = request.GET.get('issue', user_twin.primary_issue)
    matches = HormonalTwin.objects.filter(primary_issue=issue).exclude(user=request.user)
    
    # Get connection status for each match
    for match in matches:
        try:
            connection = TwinConnection.objects.get(
                Q(user1=request.user, user2=match.user) | Q(user1=match.user, user2=request.user)
            )
            match.connection_status = connection.status
        except TwinConnection.DoesNotExist:
            match.connection_status = None
    
    return render(request, 'Hormonal_Twins/find_matches.html', {
        'matches': matches,
        'current_issue': issue,
    })

@login_required
def connect_twin(request, user_id):
    """Send connection request to another twin"""
    other_user = get_object_or_404(User, id=user_id)
    
    if request.user == other_user:
        messages.error(request, 'You cannot connect with yourself!')
        return redirect('Hormonal_Twins:find_matches')
    
    # Check if already connected
    existing = TwinConnection.objects.filter(
        Q(user1=request.user, user2=other_user) | Q(user1=other_user, user2=request.user)
    ).first()
    
    if existing:
        messages.info(request, 'You already have a connection with this user!')
        return redirect('Hormonal_Twins:find_matches')
    
    if request.method == 'POST':
        message = request.POST.get('message', '')
        connection = TwinConnection.objects.create(
            user1=request.user,
            user2=other_user,
            message=message
        )
        messages.success(request, 'Connection request sent!')
        return redirect('Hormonal_Twins:find_matches')
    
    return render(request, 'Hormonal_Twins/connect_twin.html', {'other_user': other_user})

@login_required
def my_connections(request):
    """View all twin connections"""
    sent = TwinConnection.objects.filter(user1=request.user)
    received = TwinConnection.objects.filter(user2=request.user)
    
    return render(request, 'Hormonal_Twins/my_connections.html', {
        'sent': sent,
        'received': received,
    })

@login_required
def accept_connection(request, connection_id):
    """Accept a connection request"""
    connection = get_object_or_404(TwinConnection, id=connection_id)
    
    if connection.user2 != request.user:
        messages.error(request, 'You cannot accept this connection!')
        return redirect('Hormonal_Twins:my_connections')
    
    connection.status = 'connected'
    connection.save()
    messages.success(request, 'Connection accepted!')
    return redirect('Hormonal_Twins:my_connections')

@login_required
def block_connection(request, connection_id):
    """Block a connection"""
    connection = get_object_or_404(TwinConnection, id=connection_id)
    
    if connection.user2 != request.user and connection.user1 != request.user:
        messages.error(request, 'You cannot block this connection!')
        return redirect('Hormonal_Twins:my_connections')
    
    connection.status = 'blocked'
    connection.save()
    messages.success(request, 'Connection blocked!')
    return redirect('Hormonal_Twins:my_connections')

