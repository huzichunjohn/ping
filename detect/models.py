from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Ping(models.Model):
    task_id = models.UUIDField()
    ip = models.GenericIPAddressField()
    latency = models.FloatField(blank=True, null=True)
    loss = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
