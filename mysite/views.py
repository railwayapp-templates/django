# views.py
from django.shortcuts import render

def my_page(request):
    return render(request, 'index.html')  # 'my_page.html' should be in your templates folder
