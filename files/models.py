from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='files', max_length=100, blank=True)

    def __unicode__(self):
        return self.title
