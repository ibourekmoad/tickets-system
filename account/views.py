from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from account.form import RegisterCustomerForm


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        var = authenticate(request, username=username, password=password)
        if var is not None and var.is_active:
            login(request, var)
            return redirect('dashboard')
        else:
            messages.warning(request, 'Incorrect username or password')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def register_customer(request):
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer = True
            user.username = user.email
            user.save()
            messages.success(request, 'the user was successfully registered try to log in')
            return redirect('login')
        else:
            messages.warning(request, "somthing went wrong, please enter correct information")
            return redirect('register')
    else:
        form = RegisterCustomerForm()
        context = {'form': form}
        return render(request, 'accounts/register_user.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, 'you have successfully logged out')
    return redirect('login')
