from django.shortcuts import render
from django.views.generic import View
from main.models import Graph, Node, Group
from main.forms import GraphImport
# Create your views here.


class ListView(View):
    form = GraphImport

    def get(self, request):
        return render(request, "graph_list.html", {"graphs": Graph.objects.all(),
                                                   "form": self.form()})

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
                        free_nodes = graph.node_set.filter(eid__in=groupped.split(), parent_id__isnull=True)
                        free_groups = graph.group_set.filter(eid__in=groupped.split(), parent_id__isnull=True)
                        free_elements = list(free_nodes.values_list('eid', flat=True)) + \
                                         list(free_groups.values_list('eid', flat=True))
                        free_nodes.update(parent=group_obj)
                        free_groups.update(parent=group_obj)
                        diff_eids = list(set(groupped.split()).difference(set(free_elements)))
                        if diff_eids:
                            exist_elements = list(graph.group_set.filter(eid__in=diff_eids)) + \
                                             list(graph.node_set.filter(eid__in=diff_eids))
                            for obj in exist_elements:
                                obj.parent.parent = group_obj
                                obj.parent.save()
        return render(request, "graph_list.html", {"graphs": Graph.objects.all(), "form": form})