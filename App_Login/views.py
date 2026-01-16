from App_Login.forms import ProfilePic, SignUpForm, UserProfileChange
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods


# Create your views here.
@require_http_methods(["GET", "POST"])
def sign_up(request):
    form = SignUpForm()
    registered = False
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            from App_Login.models import UserProfile
            UserProfile.objects.get_or_create(user=user)
            registered = True
            messages.success(request, 'Account created successfully! Please log in.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    
    context = {'form': form, 'registered': registered}
    return render(request, 'App_Login/signup.html', context=context)


@require_http_methods(["GET", "POST"])
def login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Home:home'))
    
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
                next_url = request.GET.get('next', 'Home:home')
                return HttpResponseRedirect(reverse(next_url) if 'Home:' in next_url else reverse('Home:home'))
            else:
                messages.error(request, 'Invalid username or password.')
        else:
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
            form.save()
            changed = True

    return render(request,'App_Login/pass_change.html',context={'form':form,'changed':changed})




@login_required   
def add_pro_pic(request):
    form = ProfilePic()
    if request.method =='POST':
        form = ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit = False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/pro_pic_add.html',context={'form':form})


@login_required  
def change_pro_pic(request):
    form =ProfilePic(instance= request.user.user_profile)
    if request.method=='POST':
        form = ProfilePic(request.POST, request.FILES, instance = request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/pro_pic_add.html',context={'form':form})






