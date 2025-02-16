from django.core.management.base import BaseCommand
from inventory.models import Classroom

class Command(BaseCommand):
    help = 'Populate the Classroom model with seed data'

    def handle(self, *args, **kwargs):
        # Classroom seed data
        classroom_data = [
            ("Room 1", 20, "Admin Building", "Vacant"),
            ("Room 2", 20, "Library", "Vacant"),
            ("Room 3", 20, "Acad Building", "Vacant"),
        ]

        # Insert seed data into Classroom model
        for classroom_name, capacity, facility_type, classroom_status in classroom_data:
            Classroom.objects.create(
                classroom_name=classroom_name,
                capacity=capacity,
                facility_type=facility_type,
                classroom_status=classroom_status
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated Classroom model with seed data'))


