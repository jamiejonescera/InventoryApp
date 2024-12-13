from django.core.management.base import BaseCommand
from inventory.models import Classroom

class Command(BaseCommand):
    help = 'Populate the Classroom model with seed data'

    def handle(self, *args, **kwargs):
        # Classroom seed data
        classroom_data = [
            ("Room A", 40),
            ("Room B", 40),
            ("Room C", 40),
            ("Room D", 40),
            ("Room E", 40),
            ("Room F", 40),
            ("Room G", 40),
            ("Room H", 40),
            ("Room I", 40),
            ("Room J", 40),
        ]

        # Insert seed data into Classroom model
        for classroom_name, capacity in classroom_data:
            Classroom.objects.create(classroom_name=classroom_name, capacity=capacity)

        self.stdout.write(self.style.SUCCESS('Successfully populated Classroom model with seed data'))


