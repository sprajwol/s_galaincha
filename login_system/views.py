from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . forms import UserRegisterForm

# Create your views here.


def signup(request):
    if (request.method == 'POST'):
        form = UserRegisterForm(request.POST)
        if (form.is_valid()):
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for { username }!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'login_system/signup.html', {'form': form, 'title': 'Sign Up'})


@login_required
def profile(request):
    return render(request, 'login_system/profile.html')
