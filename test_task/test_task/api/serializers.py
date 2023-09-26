from django.contrib.auth.models import User
from rest_framework import serializers
from product.models import Product, Lesson, ViewLesson


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class LessonWithStatusAndTimeSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    viewing_time = serializers.SerializerMethodField()
    last_viewed_date = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = '__all__'


class ProductStatisticsSerializer(serializers.ModelSerializer):
    total_views = serializers.IntegerField(read_only=True)
    total_viewing_time = serializers.DecimalField(
        read_only=True,
        max_digits=10,
        decimal_places=2
    )
    total_students = serializers.IntegerField(read_only=True)
    purchase_percentage = serializers.DecimalField(
        read_only=True,
        max_digits=5,
        decimal_places=2
    )

    class Meta:
        model = Product
        fields = ('id', 'name',
                  'total_views',
                  'total_viewing_time',
                  'total_students',
                  'purchase_percentage')
