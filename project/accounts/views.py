from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate( username=email, password=password)
        if user is None:
            messages.error(request, "Invalid credentials")
            return redirect("login-page")

        login(request, user)
        messages.success(request, "Welcome to Zen")
        return redirect("home")


    return render(request, 'accounts/login.html')


def signup_view(request):
    if request.method == "POST":
        signup_form = SignupForm(request.POST)
        if not signup_form.is_valid():
            return render(request, "accounts/signup.html", {"form": signup_form})

        # user registration
        user = User.objects.create_user(
            username=signup_form.cleaned_data["email"],
            email=signup_form.cleaned_data["email"],
            password=signup_form.cleaned_data["password1"],
        )

        if not user:
            messages.error(request, "Something went wrong. Please try again later.")
            return render(request, "accounts/signup.html", {"form": signup_form})

        messages.success(request, "Signed up successfully. You can log in now.")
        return redirect("login-page")

    signup_form = SignupForm()
    return render(request, "accounts/signup.html", {"form": signup_form})


def logout_view(request):
    logout(request)
    return redirect("home")