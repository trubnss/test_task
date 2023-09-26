from django.db.models import Count, Sum, F, ExpressionWrapper, DecimalField


def annotate_product_queryset(queryset):
    """
    Аннотирует queryset агрегированными данными о продуктах.

    :param queryset: QuerySet модели Product.
    :return: QuerySet с добавленными аннотациями.
    """

    queryset = queryset.annotate(
        total_views=Count('lessons__viewlesson', distinct=True),
        total_viewing_time=Sum(ExpressionWrapper(
            F('lessons__viewlesson__viewing_time'),
            output_field=DecimalField(),
        )),
        total_students=Count('owner__accesstoproduct__user', distinct=True),
        purchase_percentage=Count('accesstoproduct', distinct=True) / F('total_students') * 100,
    )
    return queryset
