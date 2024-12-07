from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
class Classroom(models.Model):
    id = models.AutoField(primary_key=True)
    classroom_name = models.CharField(max_length=255)
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Taken', 'Taken'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        null=True,  # Allow null values
        blank=True  # Optional field in forms
    )

    def __str__(self):
        return self.classroom_name
