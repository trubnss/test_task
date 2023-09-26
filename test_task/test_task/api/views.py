from .utils import annotate_product_queryset
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from product.models import Product, Lesson, ViewLesson
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (UserRegistrationSerializer,
                          LessonWithStatusAndTimeSerializer,
                          ProductStatisticsSerializer)


class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response_data = {
            'token': access_token,
            'user_id': user.id,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class LessonListWithStatusAndTime(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = LessonWithStatusAndTimeSerializer

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs.get('product_id')

        # Получаем уроки, к которым пользователь имеет доступ в рамках указанного продукта
        accessible_lessons = Lesson.objects.filter(
            products__access_to_product__user=user,
            products__id=product_id,
        ).prefetch_related(
            'products__access_to_product',
            'viewlesson_set',
        )

        # Добавляем информацию о статусе, времени просмотра и дате последнего просмотра в каждый урок
        for lesson in accessible_lessons:
            try:
                last_viewed_lesson = ViewLesson.objects.filter(
                    user=user,
                    lesson=lesson,
                    status=True
                ).latest('viewing_time')
                lesson.last_viewed_date = last_viewed_lesson.viewing_time
                lesson.status = True
                lesson.viewing_time = last_viewed_lesson.viewing_time
            except ViewLesson.DoesNotExist:
                lesson.last_viewed_date = None
                lesson.status = False
                lesson.viewing_time = 0

        return accessible_lessons


class ProductStatisticsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    annotated_queryset = annotate_product_queryset(queryset)
    serializer_class = ProductStatisticsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
