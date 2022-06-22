from routers import CustomRouter
from .views import (StaffsListViewSet, TweetsListViewSet, PrizesListViewSet, PastAICsListViewSet, FAQListViewSet,
                    NewsListViewSet, NewsTagListViewSet, TimelineEventListViewSet, StatisticViewSet)

website_router = CustomRouter()

website_router.register(r'staffs', StaffsListViewSet, basename='staffs_api')
website_router.register(r'tweets', TweetsListViewSet, basename='tweets_api')
website_router.register(r'prizes', PrizesListViewSet, basename='prizes_api')
website_router.register(r'pastaics', PastAICsListViewSet, basename='pastaics_api')
website_router.register(r'faqs', FAQListViewSet, basename='faqs_api')
website_router.register(r'news', NewsListViewSet, basename='news_api')
website_router.register(r'newstags', NewsTagListViewSet, basename='newstags_api')
website_router.register(r'timelineevents', TimelineEventListViewSet, basename='timelineevents_api')
website_router.register(r'statistic', StatisticViewSet, basename='statistic_api')
