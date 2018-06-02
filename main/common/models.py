from django.db import models


class BaseModel(models.Model):
    eid = models.CharField(max_length=2)
    graph = models.ForeignKey('Graph', on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        abstract = True