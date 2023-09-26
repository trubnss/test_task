from django.db import models
from django.contrib.auth.models import User


class Lesson(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='название',
    )
    url_to_video = models.URLField(
        verbose_name='ссылка на видео',
    )
    viewing_duration = models.PositiveIntegerField(
        verbose_name='длительность просмотра',
    )
    last_viewed_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='дата последнего просмотра'
    )

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='название'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='владелец',
    )
    lessons = models.ManyToManyField(
        Lesson,
        related_name='products'
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']

    def __str__(self):
        return self.name


class AccessToProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user} имеет доступ к {self.product}"


class ViewLesson(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
    )
    viewing_time = models.PositiveIntegerField(
        default=0,
        verbose_name='время просмотра',

    )
    status = models.BooleanField(
        default=False,
        verbose_name='cтатус',
    )

    def __str__(self):
        return (f"{self.user} просмотрел {self.lesson} "
                f"({'Просмотрено' if self.status else 'Не просмотрено'})")

    def update_status(self):
        if int(self.viewing_time) > 0:
            percent_viewed = int((int(self.viewing_time)
                                  / int(Lesson.viewing_duration)) * 100)
            self.status = percent_viewed >= 80
        else:
            self.status = False
        self.save()
