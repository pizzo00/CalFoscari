from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserForm
from django.contrib.auth.password_validation import validate_password


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user = user_form.save(commit=False)
        if user_form.is_valid() and validate_password(user.password, user=user) is None:
            user.set_password(user.password)
            user.save()
            return redirect('home')
        else:
            return render(request, 'students/registration.html', {'user_form': user_form})

    else:
        user_form = UserForm()
        return render(request, 'students/registration.html', {'user_form': user_form })
