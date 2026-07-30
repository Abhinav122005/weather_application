from django.contrib import messages
from django.shortcuts import redirect, render
from .serializers import UserSerializer
from . models import User
from . hashing import hash_pass,check_pass
# Create your views here.


def register(req):

    if 'user_id' in req.session:
        return redirect('dashboard')
    if req.method == 'POST':
        data = req.POST.copy()

        #check both passwords
        if data['password'] != data['confirm_password']:
            messages.error(req,"Passwords donot match")
            return redirect('register')

        #check user existes or not
        if User.objects.filter(username=data['username']).exists():
            messages.error(req, 'Username already existes')
            return redirect('register')
        
        data['password'] = hash_pass(data['password'])

        data.pop("confirm_password")
        
        serializer = UserSerializer(data=data)

        # if check_password(password, user.password):
        #         request.session["user_id"] = user.id
        #         request.session["username"] = user.username
        #         return redirect("dashboard")
        if serializer.is_valid():
            serializer.save()
            messages.success(req,"Registration Successful")
            return redirect('login')
        else:
            return render(req, 'register.html',{'msg':serializer.errors})


    return render(req, 'register.html')

def login(req):

    if 'user_id' in req.session:
        return redirect('dashboard')
    
    if req.method == 'POST':
        data = req.POST.copy()
        try:
            db_data = User.objects.get(username=data['username'])

            if check_pass(data['password'],db_data.password):
                req.session["user_id"] = db_data.id
                req.session["username"] = db_data.username

                # Session expires after 1 week (7 days)
                req.session.set_expiry(60 * 60 * 24 * 7)
                return redirect('dashboard')
            else:
                return render(req, 'login.html',{'msg':'Invalid credentials'})

        except User.DoesNotExist:
            messages.error(req, 'user not found')
            return redirect("login")
    return render(req, 'login.html')


def logout(req):
    req.session.flush()
    return redirect('home')


def profile(req):
    if 'user_id' not in req.session:
        return redirect('login')

    user = User.objects.get(id=req.session['user_id'])


    return render(req, 'profile.html', {'user':user})


def edit_profile(req):
    if 'user_id' not in req.session:
        return redirect('login')

    user = User.objects.get(id=req.session['user_id'])

    if req.method == 'POST':
        data = req.POST.copy()

        if User.objects.exclude(id=user.id).filter(username=data['username']).exists():
            messages.error(req,'username already existes')
            return redirect('edit_profile')

        if User.objects.exclude(id=user.id).filter(email=data['email']).exists():
            messages.error(req, "Email already exists")
            return redirect("edit_profile")
        
        user.username=data['username']
        user.email=data['email']
        user.save()

        req.session['username']=user.username
        messages.success(req,'Profile updated successfully')
        return redirect('profile')
    
    return render(req, 'edit_profile.html',{'user':user})


def change_password(req):
    if 'user_id' not in req.session:
        return redirect('login')

    user = User.objects.get(id=req.session['user_id'])

    if req.method =='POST':
        current_password = req.POST["current_password"]
        new_password = req.POST["new_password"]
        confirm_password = req.POST["confirm_password"]

        if not check_pass(current_password, user.password):
            messages.error(req, "Current password is incorrect")
            return redirect("change_password")

        if new_password != confirm_password:
            messages.error(req, "New passwords do not match")
            return redirect("change_password")

        user.password = hash_pass(new_password)
        user.save()

        messages.success(req, "Password changed successfully")
        return redirect("profile")
    
    return render(req, 'change_password.html')