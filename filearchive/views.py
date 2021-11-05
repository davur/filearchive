from django.shortcuts import render

from django.views.generic import ListView, DetailView


from .models import *

class RootListView(ListView):
    model = Root
    paginate_by = 25

class RootDetailView(DetailView):
    model = Root
    slug_field = 'id'

class PathDetailView(DetailView):
    model = Path
    slug_field = 'id'
