from django.shortcuts import render


# @login_required
def home(request):
    return render(request, 'front/home.html')
