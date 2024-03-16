from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from django.db.models import Avg, Count, Q
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ProductSerializer,SearchHistorySerializer
from .models import Product, SearchHistory
from rest_framework import permissions
from django.core.cache import cache

class ProductCreateApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class ProductListApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price"]

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('query', None)
        if query is not None:
            queryset = queryset.filter(name__icontains=query)
            # Save search history
            SearchHistory.objects.create(user=self.request.user, query=query)
        return queryset
    # @action(
    #     methods=['get'],
    #     detail=False,
    #     url_path='profile',
    #     serializer_class=None,
    #     permission_classes=[AllowAny]
    # )

    # def get(self, request):
    #     recent_words = cache.get('recent_words')
    #     if not recent_words:
    #         recent_words = Product.objects.order_by('-created_at')[:10]
    #         cache.set('recent_words', recent_words, REDIS_TIMEOUT)
    #     serializer = ProductSerializer(recent_words, many=True)
    #     return Response(serializer.data)


# def list(self, request, *args, **kwargs):
#    query=self.filter_queryset(self.get_queryset())
#     response = super().list(request,*args,**kwargs,)
#     response_data = {'result':response.data}
#     response_data['total_amout'] = queryset.aggregate(total=Sum('price'))


# Представление для получения деталей, обновления и удаления продукта
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsSeller, ]


# Представление для получения деталей, обновления и удаления продукта


class SearchHistoryViewSet(viewsets.ModelViewSet):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer

    def perform_create(self, serializer):
        # Сохранение записи в кэше
        cache_key = f"search_history_{self.request.user.id}"
        search_history = cache.get(cache_key, [])
        search_history.append(serializer.validated_data['query'])
        cache.set(cache_key, search_history, timeout=3600)  # Время жизни кэша в секундах
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        # Получение записей из кэша
        cache_key = f"search_history_{self.request.user.id}"
        search_history = cache.get(cache_key, [])
        return Response(search_history)