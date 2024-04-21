from django.db import models

from common.models import BaseModel
from common.choises import BaseLinkType
from users.models import User


class Link(BaseModel):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField()
    image = models.ImageField(null=True, blank=True)
    link_type = models.CharField(max_length=50, choices=BaseLinkType.choices, default='website')
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Collection(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LinkCollection(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('link', 'collection')