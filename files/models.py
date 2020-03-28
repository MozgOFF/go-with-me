from django.db import models

# from account.models import User
# from event.models import Event


class Image(models.Model):
    # title = models.CharField(max_length=255)
    # file = models.FileField(upload_to='files', max_length=100, blank=True)
    #
    # def __unicode__(self):
    #     return self.title
    created_at = models.DateTimeField(auto_now_add=True)
    image_file = models.FileField(upload_to='images', blank=False, null=False)
    # uploaded_by = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    # corresponds_to_event = models.ForeignKey(Event, to_field='id', on_delete=models.CASCADE)
