from django.shortcuts import render

# Create your views here.

def login(request):
    context = {'title': 'Geekshop - Авторизация'}
    return render(request, 'authapp/login.html', context)
