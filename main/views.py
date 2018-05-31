from django.shortcuts import render
from django.views.generic import View
from main.models import Graph, Node, Group
from main.forms import GraphImport
from django.db import transaction
# Create your views here.


class ListView(View):
    form = GraphImport

    def get(self, request):
        return render(request, "graph_list.html", {"graphs": Graph.objects.all(),
                                                   "form": self.form()})

    @transaction.atomic
    def post(self, request):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            nodes_list = form.cleaned_data.get("nodes")
            groups_list = form.cleaned_data.get("groups")
            if nodes_list and groups_list:
                graph = Graph.objects.create()
                nodes = [Node(eid=i.get("eid"), text=i.get("text"), graph=graph) for i in nodes_list]
                Node.objects.bulk_create(nodes)
                for group in groups_list:
                    group_obj = Group.objects.create(eid=group.get("eid"), text=group.get("text"), graph=graph)
                    groupped = group.get("groupped")
                    if groupped:
                        graph.node_set.filter(eid__in=groupped.split()).update(parent=group_obj)
                        graph.group_set.filter(eid__in=groupped.split()).update(parent=group_obj)
        return render(request, "graph_list.html", {"graphs": Graph.objects.all(), "form": form})