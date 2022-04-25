from routers import CustomRouter
from .views import StaffsListViewSet, TweetsListViewSet

website_router = CustomRouter()

website_router.register(r'staffs', StaffsListViewSet, basename='staffs_api')
website_router.register(r'tweets', TweetsListViewSet, basename='tweets_api')
