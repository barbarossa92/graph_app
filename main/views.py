from django.shortcuts import render
from django.views.generic import View
from main.models import Graph
# Create your views here.


class ListView(View):
    def get(self, request):
        return render(request, "graph_list.html", {"graphs": Graph.objects.all()})