from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import logout
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    form=UserRegisterForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f"Welcome {username}, your account has been successfully created")
            return redirect('login')
    context={
        'form':form
    }
    return render(request,"users/register.html",context)

def logout_view(request):
    logout(request)
    return render(request,"users/logout.html")