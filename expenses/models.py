from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
import uuid


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    name= models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = 'Categories'

class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.PositiveIntegerField(default=0)
    date = models.DateField(default=now)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering:['-date']

    def __str__(self):
        return f"{self.owner}'s  expense "

    

        

