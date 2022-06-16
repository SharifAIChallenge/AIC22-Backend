from django.conf import settings


class ImageURL:
    def _image_url(self, obj):
        if not obj.image:
            return None
        path = obj.image.url
        if settings.AIC_DOMAIN not in path:
            return settings.AIC_DOMAIN + path
        return path
