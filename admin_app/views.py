from django.shortcuts import render

def home(request):
    return render(request, 'admin_app/home.html')