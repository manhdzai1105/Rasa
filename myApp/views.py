# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'pages/index.html')