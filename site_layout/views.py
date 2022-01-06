from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'site_layout/index.html')