from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import (LessonListWithStatusAndTime,
                       UserRegistrationViewSet,
                       ProductStatisticsViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'register', UserRegistrationViewSet, basename='user-registration')
router_v1.register(r'lessons', LessonListWithStatusAndTime, basename='lesson-list')
router_v1.register(r'products', ProductStatisticsViewSet, basename='product-statistics')
router_v1.register(r'products/(?P<product_id>\d+)/lessons',
                   LessonListWithStatusAndTime, basename='product-lessons')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
