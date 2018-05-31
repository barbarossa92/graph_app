from django.conf.urls import url
from main.views import ListView


urlpatterns = [
    url(r'^', ListView.as_view(), name='graph_list')
]