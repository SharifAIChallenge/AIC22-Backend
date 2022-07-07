from django.core.management import BaseCommand

from PIL import Image
from website.models import Staff


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for staff in Staff.objects.all():
            image_path = staff.image.path
            Image.open(image_path).convert("RGB").save(image_path, optimize=True)
