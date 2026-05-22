from django.shortcuts import render

def home(request):
    return render(request, "lotto/home.html")
