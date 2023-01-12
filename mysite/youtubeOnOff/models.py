from django.db import models

# Create your models here.

class OnOff(models.Model):
    title = models.CharField(max_length=50)
    modified_time = models.DateTimeField('Modified TIme')
    video_id = models.CharField(max_length=100)
    work_time = models.DateTimeField('Work Time')
    privacy_status = models.CharField(max_length=20)
