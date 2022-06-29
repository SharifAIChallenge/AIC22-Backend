from django.conf import settings


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
