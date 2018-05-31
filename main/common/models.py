from django.db import models


class BaseModel(models.Model):
    eid = models.CharField(max_length=2)
    graph = models.ForeignKey('Graph')
    text = models.TextField()

    class Meta:
        abstract = True