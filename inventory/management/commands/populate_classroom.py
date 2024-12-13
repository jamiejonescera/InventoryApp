from django.core.management.base import BaseCommand
from inventory.models import Classroom

class Command(BaseCommand):
    help = 'Populate the Classroom model with seed data'

    def handle(self, *args, **kwargs):
        # Classroom seed data
        classroom_data = [
            ("Room A", "Available"),
            ("Room B", "Available"),
            ("Room C", "Available"),
            ("Room D", "Available"),
            ("Room E", "Available"),
            ("Room F", "Available"),
            ("Room G", "Available"),
            ("Room H", "Available"),
            ("Room I", "Available"),
            ("Room J", "Available"),
        ]
        
        # Insert seed data into Classroom model
        for classroom_name, status in classroom_data:
            Classroom.objects.create(classroom_name=classroom_name, status=status)

        self.stdout.write(self.style.SUCCESS('Successfully populated Classroom model with seed data'))
