from django.db import models

from django.contrib.auth.models import AbstractUser

class AdvUser(AbstractUser):#своя модель пользователя
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошёл активацию')
    send_messages = models.BooleanField(default=True, verbose_name='Слать оповещение о новых комментариях')

    class Meta:
        pass

class Rubric(models.Model):#таблица в БД для рубрик
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric',
    on_delete=models.PROTECT, null=True, blank=True,
    verbose_name='Надрубрики')

class SuperRubricManager(models.Manager):#диспетчер рубрик
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)

class SuperRubric(Rubric):#надрубрика
    objects = SuperRubricManager()

    def __str__(self):
        return self.name
    
    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрика'

class SubRubricManager(models.Manager):#диспетчер записей подрубрики
    def qut_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)

class SubRubric(Rubric):#подрубрика
    objects = SubRubricManager()

    def __str__(self):
        return '%s - %s' % (self.super_rubric, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'

