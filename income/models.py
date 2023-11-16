from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.timezone import now
# Create your models here.

class Income(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.PositiveIntegerField(default=1)
    source = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateField(default=now)

    def __str__(self):
        return f'{self.user} - {self.amount}'
    
    class Meta:
        ordering=['-created']
