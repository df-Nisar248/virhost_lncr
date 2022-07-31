from django.shortcuts import render ,redirect

from . models import Remembprot

def home(request):
    return render(request,'rememb_prot/home.html')
