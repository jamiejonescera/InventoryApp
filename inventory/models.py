from django.db import models
from django.utils.timezone import now  # Import `now` from django.utils.timezone

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, unique=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product_name  # Changed 'self.name' to 'self.product_name'

class Classroom(models.Model):
    id = models.AutoField(primary_key=True)
    classroom_name = models.CharField(max_length=255)
    capacity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.classroom_name
    

class Request(models.Model):
    requester_name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')], default='Pending')
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
