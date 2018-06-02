from django.db import transaction
from django.shortcuts import render
from django.views.generic import View, DetailView
from main.models import Graph, Node, Group
from main.forms import GraphImport
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
                created_groups = list()
                nodes = [Node(eid=i.get("eid"), text=i.get("text"), graph=graph) for i in nodes_list]
                for group in groups_list:
                    group_obj = Group.objects.create(eid=group.get("eid"), text=group.get("text"), graph=graph)
                    created_groups.append(group_obj)
                    groupped = group.get("groupped")
                    if groupped:
                        free_elements = list(filter(lambda n: n.eid in groupped.split() and not n.parent, nodes + created_groups))
                        for element in free_elements:
                            element.parent = group_obj
                            element.save()
                        diff_eids = list(set(groupped.split()).difference(set([i.eid for i in free_elements])))
                        if diff_eids:
                            exist_elements = list(filter(lambda el: el.eid in diff_eids, nodes + created_groups))
                            for obj in exist_elements:
                                tmp_obj = obj
                                while tmp_obj.parent != None:
                                    tmp_obj = tmp_obj.parent
                                else:
                                    if tmp_obj != group_obj:
                                        tmp_obj.parent = group_obj
                                        tmp_obj.save()
        return render(request, "graph_list.html", {"graphs": Graph.objects.all(), "form": form})


class GraphDetail(DetailView):
    queryset = Graph.objects.all()
    model = Graph
    template_name = "graph_detail.html"