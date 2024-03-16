from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'search-history', SearchHistoryViewSet)

urlpatterns = [
    path("product/list/", ProductListApiView.as_view(), name="product-list"),
    path("product/create/", ProductCreateApiView.as_view(), name="product-create"),
    path('', include(router.urls)),
]
