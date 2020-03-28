from django.db import models


class Comment(models.Model):
    content = models.TextField(verbose_name="Content")
    parent = models.ForeignKey('self', null=True, blank=None, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

