from django.conf import settings
from PIL import Image
from django.db.models.fields.files import ImageFieldFile


def compress_image(image: ImageFieldFile):
    image: Image.Image = Image.open(image.path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
        image.save(image.path)


class ImageURL:
    def _image_url(self, obj):
        if not obj.image:
            return None
        path = obj.image.url
        if settings.AIC_BACKEND_DOMAIN not in path:
            return settings.AIC_BACKEND_DOMAIN + path
        return path

    def _resume_url(self, obj):
        if not obj.resume:
            return None
        path = obj.resume.url
        if settings.AIC_BACKEND_DOMAIN not in path:
            return settings.AIC_BACKEND_DOMAIN + path
        return path
