from django.shortcuts import render

def home(request):
    return render(request, 'donneur/home.html')