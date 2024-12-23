# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myApp.models import NganhTuyenSinh
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'pages/index.html')

@api_view(['GET'])
def so_luong_nganh(request):
    so_luong_nganh = NganhTuyenSinh.objects.count()
    return Response({"so_luong_nganh": so_luong_nganh})