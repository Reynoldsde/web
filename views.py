from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from adminpanel.models import invitation_code
from .models import account
from django.contrib.auth import update_session_auth_hash


def create_userid():
    status = True
    id = 0
    while status:
        id = id + 1  
        if account.objects.filter(userid=id).exists():
            pass
        else:
            status = False
            return(id)

def login_user(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                if request.user.is_admin:
                    return redirect('/adminpanel/withdrawal-requests/')
                else:
                    return redirect('/')
            else:
                messages.error(request, ("invalid credentials"))
                return redirect('/login/')                
        else:
            messages.error(request, ("invalid credentials"))
            return redirect('/login/')
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect("/adminpanel/withdrawal-requests/")
        else:
            return redirect("/")
    else:
        return render(request, 'login.html')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']

        password = request.POST['password']
        confirmpass = request.POST['confirmpass']

        invitation_codes = request.POST["invitation_code"]


        
        if password == confirmpass:
            if len(password) <= 5:
                messages.error(request, ("Password must contain more than 8 characters"))
                return redirect('/signup/')
            else:
                passwordhashed = make_password(password)
                
                if account.objects.filter(email=email).exists():
                    messages.error(request, ("The email you are using is already associated with another account."))
                    return redirect('/signup')
                else:
                    code = invitation_code.objects.filter(code=invitation_codes).first()
                    if code and code.activated == False:
                        newuser = account(userid=create_userid(),  username=email, name=name , email=email, password=passwordhashed)
                        newuser.is_active = True
                        newuser.save()
                        code.activated = True
                        code.used_by = newuser
                        code.save()
                        messages.success(request, ("Signed up successfully."))
                        return redirect('/login')
                    else:
                        messages.error(request, "Invitation Code Is Invalid")
                        return redirect('/signup')
        else:
            messages.error(request, ("Your password and confirmation password do not match."))
            return redirect('/signup/')
    else:
        return render(request, 'signup.html')


@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect("/")


@login_required(login_url='/login')
def update_profile(request):
    if request.user.is_admin == False:
        return redirect("/")
    
    if request.method == 'POST':        
        user_pk = request.POST["user_pk"]
        new_password = request.POST['new_password']
        conf_password = request.POST['conf_password']

        user = account.objects.get(pk=user_pk)

        if new_password == conf_password:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            
            messages.success(request, 'Password changed successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        else:
            messages.error(request, 'New passwords do not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))