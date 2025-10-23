from django.db import models

class Price(models.Model):
    time_period = models.CharField(max_length=100, verbose_name="Временной период")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.CharField(max_length=50, verbose_name="Продолжительность")
    is_dinner_price = models.BooleanField(default=False, verbose_name="Обеденная цена")
    
    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"
    
    def __str__(self):
        return f"{self.time_period} - {self.price} руб."

class ClubInfo(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название клуба")
    address = models.CharField(max_length=300, verbose_name="Адрес")
    description = models.TextField(verbose_name="Описание")
    
    class Meta:
        verbose_name = "Информация о клубе"
        verbose_name_plural = "Информация о клубе"
    
    def __str__(self):
        return self.name