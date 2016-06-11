from django.db import models

class Ping(models.Model):
    task_id = models.UUIDField()
    ip = models.IPAddressField()
    latency = models.IntegerField()
    loss = models.IntegerField(min_value=0, max_value=100)
