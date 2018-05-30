from django.db import models
from main.common.models import BaseModel

# Create your models here.


class Graph(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Графы"


class Group(BaseModel):
    parent = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Группы"


class Node(BaseModel):
    parent = models.ForeignKey('Group', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Ноды"