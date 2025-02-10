from django.db import models
from django.utils.timezone import now  # Import `now` from django.utils.timezone
from django.utils.timezone import now



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
    facility_type = models.CharField(max_length=255)
    classroom_status = models.CharField(max_length=20, blank=True, null= True)

    def __str__(self):
        return self.classroom_name
    
class Request(models.Model):
    id = models.AutoField(primary_key=True)
    staff_name = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    quantity_requested = models.IntegerField(default=0)
    purpose = models.TextField(max_length=255)
    contact_number = models.CharField(max_length=20, blank=True, null=True)  # Changed IntegerField to CharField to support dashes
    request_status = models.CharField(max_length=50, choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Denied", "Denied")])
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.staff_name} - {self.product_name} ({self.quantity_requested})"
