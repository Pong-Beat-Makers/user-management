from django.shortcuts import render


# Create your views here.
def login(request):
    return render(request, 'social_login/home.html')
