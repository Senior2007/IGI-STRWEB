from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


phone_validator = RegexValidator(
    regex=r'^\+375 \((25|29|33|44)\) \d{3}-\d{2}-\d{2}$',
    message='Телефон должен быть в формате +375 (29) XXX-XX-XX.',
)


def validate_adult(value):
    today = timezone.localdate()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError('Возраст клиента или сотрудника должен быть не меньше 18 лет.')


def validate_not_future(value):
    if value > timezone.localdate():
        raise ValidationError('Дата не может быть в будущем.')


class TimeStampedModel(models.Model):
    created_at_utc = models.DateTimeField(default=timezone.now, editable=False)
    updated_at_utc = models.DateTimeField(auto_now=True)
    created_at_timezone = models.CharField(max_length=64, default=settings.TIME_ZONE, editable=False)
    created_at_local_text = models.CharField(max_length=32, blank=True, editable=False)
    updated_at_local_text = models.CharField(max_length=32, blank=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.created_at_local_text:
            self.created_at_local_text = timezone.localtime(self.created_at_utc).strftime('%d/%m/%Y %H:%M')
        self.created_at_timezone = settings.TIME_ZONE
        self.updated_at_local_text = timezone.localtime(now).strftime('%d/%m/%Y %H:%M')
        super().save(*args, **kwargs)


class CompanyInfo(TimeStampedModel):
    title = models.CharField(max_length=120)
    content = models.TextField()
    year = models.PositiveIntegerField(null=True, blank=True)
    logo_url = models.URLField(blank=True)

    class Meta:
        ordering = ['year', 'title']
        verbose_name = 'Информация о компании'
        verbose_name_plural = 'Информация о компании'

    def __str__(self):
        return self.title


class NewsArticle(TimeStampedModel):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=190, unique=True)
    summary = models.CharField(max_length=260)
    content = models.TextField()
    image_url = models.URLField(blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])


class Term(TimeStampedModel):
    title = models.CharField(max_length=120)
    definition = models.TextField()
    added_on = models.DateField(default=timezone.localdate, validators=[validate_not_future])

    class Meta:
        ordering = ['title']
        verbose_name = 'Термин'
        verbose_name_plural = 'Словарь терминов'

    def __str__(self):
        return self.title


class Vacancy(TimeStampedModel):
    title = models.CharField(max_length=120)
    description = models.TextField()
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-is_active', 'title']
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def clean(self):
        if self.salary_max and self.salary_min and self.salary_max < self.salary_min:
            raise ValidationError('Максимальная зарплата не может быть меньше минимальной.')

    def __str__(self):
        return self.title


class ProductType(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Типы товаров'

    def __str__(self):
        return self.name


class Manufacturer(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    country = models.CharField(max_length=80)
    website = models.URLField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Изготовитель'
        verbose_name_plural = 'Изготовители'

    def __str__(self):
        return self.name


class Supplier(TimeStampedModel):
    name = models.CharField(max_length=140, unique=True)
    address = models.CharField(max_length=220)
    phone = models.CharField(max_length=20, validators=[phone_validator])
    email = models.EmailField()

    class Meta:
        ordering = ['name']
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.name


class Part(TimeStampedModel):
    sku = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=160)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name='parts')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, related_name='parts')
    suppliers = models.ManyToManyField(Supplier, through='Supply', related_name='parts')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def clean(self):
        if self.quantity < 0:
            raise ValidationError('Количество не может быть отрицательным.')

    def __str__(self):
        return f'{self.sku} - {self.name}'

    def get_absolute_url(self):
        return reverse('part_detail', args=[self.pk])


class Supply(TimeStampedModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    purchase_date = models.DateField(default=timezone.localdate, validators=[validate_not_future])
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        ordering = ['-purchase_date']
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'

    def __str__(self):
        return f'{self.supplier} -> {self.part}'


class Client(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='client_profile')
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    birth_date = models.DateField(validators=[validate_adult, validate_not_future])
    phone = models.CharField(max_length=20, validators=[phone_validator])
    email = models.EmailField()
    address = models.CharField(max_length=220)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Employee(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee_profile')
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    position = models.CharField(max_length=120)
    birth_date = models.DateField(validators=[validate_adult, validate_not_future])
    phone = models.CharField(max_length=20, validators=[phone_validator])
    email = models.EmailField()
    photo_url = models.URLField(blank=True)
    responsibilities = models.TextField()

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Sale(TimeStampedModel):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='sales')
    part = models.ForeignKey(Part, on_delete=models.PROTECT, related_name='sales')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')
    sold_at = models.DateTimeField(default=timezone.now)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        ordering = ['-sold_at']
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def clean(self):
        if self.part_id and self.quantity and self.quantity > self.part.quantity:
            raise ValidationError('На складе недостаточно товара для продажи.')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.full_clean()
        if is_new:
            self.part.quantity -= self.quantity
            self.part.save(update_fields=['quantity', 'updated_at_utc', 'updated_at_local_text'])
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.part} x {self.quantity}'


class Review(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=120)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField()
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at_utc']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.name}: {self.rating}'


class PromoCode(TimeStampedModel):
    code = models.CharField(max_length=40, unique=True)
    description = models.TextField()
    discount_percent = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)])
    starts_at = models.DateField()
    ends_at = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-is_active', 'ends_at']
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def clean(self):
        if self.ends_at < self.starts_at:
            raise ValidationError('Дата окончания не может быть раньше даты начала.')

    @property
    def is_current(self):
        today = timezone.localdate()
        return self.is_active and self.starts_at <= today <= self.ends_at

    def __str__(self):
        return self.code

# Create your models here.
