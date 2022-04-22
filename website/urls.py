from routers import CustomRouter
from .views import StaffsListViewSet, FAQListViewSet

website_router = CustomRouter()

website_router.register(r'staffs', StaffsListViewSet, basename='staffs_api')
website_router.register(r'faqs', FAQListViewSet, basename='faqs_api')
