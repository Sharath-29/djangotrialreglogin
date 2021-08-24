from django.shortcuts import render
from goal_app.forms import UserForm, UserProfileInfoForm

#
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request,'goal_app/index.html')

@login_required
def special(request):
    return HttpResponse('YOU ARE LOGGED IN , WELCOME BACK!')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user 

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    goal_dict = {'user_form':user_form,'profile_form':profile_form,'registered': registered} 
    return render(request,'goal_app/registration.html',context=goal_dict)


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print("someone tried to login and failed")
            print("username {} , password {}".format(username,password))
    else:
        return render(request,'goal_app/login.html',{})
    
