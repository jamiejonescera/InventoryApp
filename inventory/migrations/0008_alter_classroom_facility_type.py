# Generated by Django 5.1 on 2025-02-10 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_classroom_classroom_status_classroom_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='facility_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
