from django.shortcuts import render, redirect
from accounts.forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# ---------------- registration ----------------


def account_register(request):
    if request.user.is_authenticated:
        return redirect("products:product-list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            return redirect("products:product-list")
        
    else:
        form = RegisterForm()
        
    context = {
        "form": form
    }
    
    return render(request, "accounts/registration/register.html", context)

def account_login(request):
    if request.user.is_authenticated:
        return redirect("products:product-list")
    
    if request.method == "POST":
        form = LoginForm(
            request,
            data=request.POST
        )
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            return redirect("products:product-list")
  
    else:
        form = LoginForm(request)
    
    context = {
        "form": form
    }
        
    return render(request, "accounts/registration/login.html", context)

@login_required
def account_logout(request):
    logout(request)
    return redirect("products:product-list")