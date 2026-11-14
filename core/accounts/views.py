from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from accounts.forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Profile, Address
from accounts.forms import ProfileForm, AddressForm, EmailForm


# ---------------- registration ----------------


def account_register(request):
    if request.user.is_authenticated:
        return redirect("products:list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            return redirect("products:list")
        
    else:
        form = RegisterForm()
        
    context = {
        "form": form
    }
    
    return render(request, "accounts/registration/register.html", context)

def account_login(request):
    if request.user.is_authenticated:
        return redirect("products:list")
    
    if request.method == "POST":
        form = LoginForm(
            request,
            data=request.POST
        )
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            return redirect("products:list")
  
    else:
        form = LoginForm()
    
    context = {
        "form": form
    }
        
    return render(request, "accounts/registration/login.html", context)

@login_required
def account_logout(request):
    logout(request)
    return redirect("products:list")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile/profile.html"
    

class EditPersonal(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy("accounts:profile")
    template_name = "accounts/personal/personal_form.html"
    
    def get_object(self):
        return get_object_or_404(
            Profile,
            user=self.request.user
        ) 
    

class EditEmail(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = EmailForm
    success_url = reverse_lazy("accounts:profile")
    template_name = "accounts/personal/personal_form.html"
    
    def get_object(self):
        return get_object_or_404(
            Profile,
            user=self.request.user
        )


class UserAddresses(LoginRequiredMixin, ListView):
    template_name = "accounts/address/addresses.html"
    context_object_name = "addresses"
    
    def get_queryset(self):
        return Address.objects.get_user_addresses(self.request.user)


class AddAddress(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    success_url = reverse_lazy("accounts:addresses")
    # success_message = "Post created successfully."
    template_name = "accounts/address/address_form.html"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditAddress(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressForm
    success_url = reverse_lazy("accounts:addresses")
    # success_message = "Post created successfully."
    template_name = "accounts/address/address_form.html"
    
    def get_queryset(self):  
        return Address.objects.filter(
            user=self.request.user
        )


class DeleteAddress(LoginRequiredMixin, DeleteView):
    model = Address
    success_url = reverse_lazy("accounts:addresses")
    # success_message = "Post created successfully."
    template_name = "accounts/address/address_confirm_delete.html"
    
    def get_queryset(self):  
        return Address.objects.filter(
            user=self.request.user
        )
