from routers import CustomRouter
from views import StaffsListViewSet

website_router = CustomRouter()

website_router.register(r'staffs', StaffsListViewSet, basename='staffs_api')
