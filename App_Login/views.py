from App_Login.forms import ProfilePic, SignUpForm, UserProfileChange
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.http import HttpResponse
import time


def rate_limit_check(request, action='login'):
    ip = request.META.get('REMOTE_ADDR')
    cache_key = f'rate_limit_{action}_{ip}'
    attempts = cache.get(cache_key, 0)
    
    if attempts >= 5:
        return True, attempts
    return False, attempts

def increment_rate_limit(request, action='login'):
    ip = request.META.get('REMOTE_ADDR')
    cache_key = f'rate_limit_{action}_{ip}'
    attempts = cache.get(cache_key, 0)
    cache.set(cache_key, attempts + 1, 300)


@require_http_methods(["GET", "POST"])
def sign_up(request):
    is_limited, attempts = rate_limit_check(request, 'signup')
    if is_limited:
        messages.error(request, 'Too many signup attempts. Please try again in 5 minutes.')
        return render(request, 'App_Login/signup.html', context={'form': SignUpForm()})
    
    form = SignUpForm()
    registered = False
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            from App_Login.models import UserProfile
            UserProfile.objects.get_or_create(user=user)
            registered = True
            messages.success(request, 'Account created successfully! Please log in.')
            cache.delete(f'rate_limit_signup_{request.META.get("REMOTE_ADDR")}')
        else:
            increment_rate_limit(request, 'signup')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    
    context = {'form': form, 'registered': registered}
    return render(request, 'App_Login/signup.html', context=context)


@require_http_methods(["GET", "POST"])
def login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Home:home'))
    
    is_limited, attempts = rate_limit_check(request, 'login')
    if is_limited:
        messages.error(request, 'Too many login attempts. Please try again in 5 minutes.')
        return render(request, 'App_Login/login.html', context={'form': AuthenticationForm()})
    
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                cache.delete(f'rate_limit_login_{request.META.get("REMOTE_ADDR")}')
                next_url = request.GET.get('next', 'Home:home')
                return HttpResponseRedirect(reverse(next_url) if 'Home:' in next_url else reverse('Home:home'))
            else:
                increment_rate_limit(request, 'login')
                messages.error(request, 'Invalid username or password.')
        else:
            increment_rate_limit(request, 'login')
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'App_Login/login.html', context={'form': form})



@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:signin'))




@login_required
def profile(request):
    return render(request, 'App_Login/profile.html', context={})


@login_required   
def user_change(request):
    current_user = request.user
   
    form = UserProfileChange(instance=current_user)
    if request.method =='POST':
        form = UserProfileChange(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = UserProfileChange(instance=current_user)  
    return render(request, 'App_Login/change_profile.html', context={'form':form})



@login_required   
def pass_change(request):
    current_user= request.user
    changed = False
    form = PasswordChangeForm(current_user)

    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            changed = True
            messages.success(request, 'Your password has been changed successfully!')

    return render(request,'App_Login/pass_change.html',context={'form':form,'changed':changed})




@login_required   
def add_pro_pic(request):
    form = ProfilePic()
    if request.method =='POST':
        form = ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('profile_pic')
            if uploaded_file and uploaded_file.size > 5242880:
                messages.error(request, 'File size must be less than 5MB.')
                return render(request, 'App_Login/pro_pic_add.html',context={'form':form})
            
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
            if uploaded_file and uploaded_file.content_type not in allowed_types:
                messages.error(request, 'Only image files (JPEG, PNG, GIF, WebP) are allowed.')
                return render(request, 'App_Login/pro_pic_add.html',context={'form':form})
            
            user_obj = form.save(commit = False)
            user_obj.user = request.user
            user_obj.save()
            messages.success(request, 'Profile picture added successfully!')
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/pro_pic_add.html',context={'form':form})


@login_required  
def change_pro_pic(request):
    form =ProfilePic(instance= request.user.user_profile)
    if request.method=='POST':
        form = ProfilePic(request.POST, request.FILES, instance = request.user.user_profile)
        if form.is_valid():
            uploaded_file = request.FILES.get('profile_pic')
            if uploaded_file and uploaded_file.size > 5242880:
                messages.error(request, 'File size must be less than 5MB.')
                return render(request, 'App_Login/pro_pic_add.html',context={'form':form})
            
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
            if uploaded_file and uploaded_file.content_type not in allowed_types:
                messages.error(request, 'Only image files (JPEG, PNG, GIF, WebP) are allowed.')
                return render(request, 'App_Login/pro_pic_add.html',context={'form':form})
            
            form.save()
            messages.success(request, 'Profile picture updated successfully!')
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/pro_pic_add.html',context={'form':form})






