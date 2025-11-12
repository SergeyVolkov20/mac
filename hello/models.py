from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from decimal import Decimal


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


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
  
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_user_set', 
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  
        related_query_name='user',
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.email} ({self.phone_number})"

class Position(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Зарплата',
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
    
    def __str__(self):
        return self.title

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    position = models.ForeignKey(Position, on_delete=models.PROTECT, verbose_name='Должность')
    passport = models.CharField(max_length=100, verbose_name='Паспорт')
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    email = models.EmailField(verbose_name='Почта')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    
    class Meta:
        verbose_name = 'Персонал'
        verbose_name_plural = 'Персонал'
    
    def __str__(self):
        return self.full_name

class Shift(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name='Персонал')
    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    
    class Meta:
        verbose_name = 'Смена'
        verbose_name_plural = 'Смены'
    
    def __str__(self):
        return f"{self.staff.full_name} - {self.start_time.strftime('%d.%m.%Y %H:%M')}"

class GameStation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активна'),
        ('maintenance', 'На обслуживании'),
        ('inactive', 'Неактивна'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Название')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active',
        verbose_name='Статус'
    )
    
    class Meta:
        verbose_name = 'Игровая станция'
        verbose_name_plural = 'Игровые станции'
    
    def __str__(self):
        return self.name

class GameZone(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True)
    hourly_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Часовая стоимость',
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    characteristics = models.TextField(verbose_name='Характеристики', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    game_station = models.ForeignKey(
        GameStation, 
        on_delete=models.CASCADE, 
        verbose_name='Игровая станция'
    )
    
    class Meta:
        verbose_name = 'Игровая зона'
        verbose_name_plural = 'Игровые зоны'
    
    def __str__(self):
        return self.name

class Visitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    
    class Meta:
        verbose_name = 'Посетитель'
        verbose_name_plural = 'Посетители'
    
    def __str__(self):
        return self.full_name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('confirmed', 'Подтверждено'),
        ('active', 'Активно'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name='Статус'
    )
    total_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Стоимость',
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    guest_count = models.PositiveIntegerField(verbose_name='Кол-во гостей')
    game_zone = models.ForeignKey(GameZone, on_delete=models.CASCADE, verbose_name='Игровая зона')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
    
    def __str__(self):
        return f"Бронирование #{self.id} - {self.user.email}"

class Visit(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, verbose_name='Посетитель')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name='Бронирование')
    arrival_time = models.DateTimeField(verbose_name='Время прихода')
    departure_time = models.DateTimeField(null=True, blank=True, verbose_name='Время ухода')
    
    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'
    
    def __str__(self):
        return f"Посещение {self.visitor.full_name} - {self.arrival_time.strftime('%d.%m.%Y %H:%M')}"