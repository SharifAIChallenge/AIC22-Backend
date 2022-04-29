from routers import CustomRouter
from .views import StaffsListViewSet, TweetsListViewSet, PrizesListViewSet, PastAICsListViewSet, FAQListViewSet

website_router = CustomRouter()

website_router.register(r'staffs', StaffsListViewSet, basename='staffs_api')
website_router.register(r'tweets', TweetsListViewSet, basename='tweets_api')
website_router.register(r'prizes', PrizesListViewSet, basename='prizes_api')
website_router.register(r'pastaics', PastAICsListViewSet, basename='pastaics_api')
website_router.register(r'faqs', FAQListViewSet, basename='faqs_api')
