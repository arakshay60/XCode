from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import RegForm
from django.contrib.auth.decorators import login_required
from .forms import ProfForm
# Create your views here.
def loginPage(request):
   
   if request.user.is_authenticated:
      return redirect('home')
   else:
      if request.method=="POST":
         username=request.POST.get("username")
         password=request.POST.get("password")
         user=authenticate(request,username=username,password=password)
         
         if user is not None:
            login(request,user)
            return redirect("home")
         else:
            messages.error(request,'Invalid login credentials')
      context={}     
      return render(request,'Users/login.html',context)
   


def logoutPage(request):
   logout(request)
   return redirect('login')


def regPage(request):
    form=RegForm()  
    if request.method=='POST':
        form=RegForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account has been created succesfully")
            return redirect('login')
        
      
    return render(request,'Users/register.html',{'form':form})


@login_required(login_url='login')
def userProfile(request):
   user=request.user
   context={'user':user}
   return render(request,'Users/profile.html',context)

@login_required(login_url='login')
def editProfile(request):
    form=ProfForm()
    user=request.user
    if request.method=='POST':
       form=ProfForm(request.POST,request.FILES,instance=user)
       if form.is_valid():
          form.save()
          return redirect('profile')
    context={'user':user,'form':form}
    return render(request,'Users/editprofile.html',context)