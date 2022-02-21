from django.shortcuts import render
from django.views.generic import View


class Index(View):
    """
    A whole app that returns the index page. 
    """

    def get(self, request, *args, **kwargs):
        return render(request, 'site_layout/index.html')
