from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages

from store.forms import CustomUserForm

# Create your Authview here.


def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Registered Successfully! Login To Continue")
            return redirect('/login')
    context = {'form': form}
    return render(request, "store/auth/register.html", context)

# Messages to appear when user has logged in and out successfully


def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, "You're currently logged in already")
        return redirect('/')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            passwd = request.POST.get('password')

            user = authenticate(request, username=name, password=passwd)

            if user is not None:
                login(request, user)
                messages.success(request, "Login In Successfully")
                return redirect('/')
            else:
                messages.error(request, "Invalid Username Or Password")
                return redirect('/login')

        return render(request, "store/auth/login.html")


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out Successfully")
    return redirect('/')
