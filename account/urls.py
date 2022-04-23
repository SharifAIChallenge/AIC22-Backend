from routers import CustomRouter
from .views import ProfileAPIView, HideProfileInfoAPIView

website_router = CustomRouter()

website_router.register(r'profile', ProfileAPIView, basename='profile_api')
website_router.register(r'profile/hide', HideProfileInfoAPIView, basename='hide_profile_api')
