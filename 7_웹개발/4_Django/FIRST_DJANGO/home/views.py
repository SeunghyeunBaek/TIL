from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')


def contact(request):
    return render(request, 'home/contact.html')


def help_me(request):
    return render(request, 'home/help_me.html')

