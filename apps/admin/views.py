from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

class vAdmin(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/home.html')