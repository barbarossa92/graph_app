from django.conf.urls import url
from main.views import ListView, GraphDetail


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', GraphDetail.as_view(), name='graph_detail'),
    url(r'^', ListView.as_view(), name='graph_list')
]