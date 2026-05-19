from datetime import date
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .forms import RegistrationForm
from .models import (
    Client,
    CompanyInfo,
    Employee,
    Manufacturer,
    NewsArticle,
    Part,
    ProductType,
    PromoCode,
    Review,
    Sale,
    Supplier,
    Term,
    Vacancy,
    validate_adult,
)


class ValidationTests(TestCase):
    def test_validate_adult_rejects_underage(self):
        with self.assertRaises(ValidationError):
            validate_adult(date.today().replace(year=date.today().year - 17))

    def test_registration_form_rejects_wrong_phone(self):
        form = RegistrationForm(
            data={
                'username': 'new_client',
                'first_name': 'Иван',
                'last_name': 'Петров',
                'birth_date': '1999-01-01',
                'phone': '80291234567',
                'email': 'client@example.com',
                'address': 'Минск',
                'password1': 'StrongPass12345',
                'password2': 'StrongPass12345',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)


class ShopViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('client', password='client12345')
        self.client_profile = Client.objects.create(
            user=self.user,
            first_name='Иван',
            last_name='Петров',
            birth_date=date(1990, 1, 1),
            phone='+375 (29) 123-45-67',
            email='client@example.com',
            address='Минск',
        )
        self.product_type = ProductType.objects.create(name='Фильтры')
        self.manufacturer = Manufacturer.objects.create(name='Parts Co', country='Germany')
        self.supplier = Supplier.objects.create(
            name='Поставщик',
            address='Минск',
            phone='+375 (33) 123-45-67',
            email='supplier@example.com',
        )
        self.part = Part.objects.create(
            sku='T-1',
            name='Фильтр',
            product_type=self.product_type,
            manufacturer=self.manufacturer,
            price=Decimal('50.00'),
            quantity=5,
            description='Тестовая запчасть',
        )
        self.employee = Employee.objects.create(
            first_name='Анна',
            last_name='Смирнова',
            position='Менеджер',
            birth_date=date(1990, 1, 1),
            phone='+375 (44) 111-22-33',
            email='employee@example.com',
            responsibilities='Консультации клиентов.',
        )
        CompanyInfo.objects.create(title='Открытие', content='История компании.', year=2020)
        NewsArticle.objects.create(
            title='Поступили новые фильтры',
            slug='new-filters',
            summary='Краткая новость о поставке.',
            content='Полный текст новости.',
            published_at=timezone.now(),
        )
        Term.objects.create(title='Артикул', definition='Уникальный код товара.')
        Vacancy.objects.create(title='Менеджер', description='Работа с заказами.', salary_min=1000, salary_max=1500)
        Review.objects.create(user=self.user, name='Иван Петров', rating=5, text='Хороший магазин и быстрый подбор.')
        PromoCode.objects.create(
            code='TEST10',
            description='Тестовая скидка.',
            discount_percent=10,
            starts_at=date(2026, 1, 1),
            ends_at=date(2026, 12, 31),
        )

    def test_public_parts_page_available(self):
        response = self.client.get(reverse('part_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Фильтр')

    def test_api_requires_login(self):
        response = self.client.get(reverse('parts_api'))
        self.assertEqual(response.status_code, 302)

    def test_logged_user_can_buy_part(self):
        self.client.login(username='client', password='client12345')
        response = self.client.post(reverse('sale_create'), {'part': self.part.pk, 'quantity': 2})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Sale.objects.count(), 1)
        self.part.refresh_from_db()
        self.assertEqual(self.part.quantity, 3)

    def test_staff_crud_is_forbidden_for_regular_user(self):
        self.client.login(username='client', password='client12345')
        response = self.client.get(reverse('part_create'))
        self.assertEqual(response.status_code, 302)

    def test_staff_can_soft_delete_part(self):
        staff = User.objects.create_user('staff', password='staff12345', is_staff=True)
        self.client.force_login(staff)
        response = self.client.post(reverse('part_delete', args=[self.part.pk]))
        self.assertEqual(response.status_code, 302)
        self.part.refresh_from_db()
        self.assertFalse(self.part.is_active)

    def test_required_public_pages_are_available(self):
        url_names = [
            'home',
            'about',
            'news_list',
            'terms',
            'contacts',
            'privacy',
            'vacancies',
            'reviews',
            'promos',
        ]
        for name in url_names:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_news_detail_and_part_detail_are_available(self):
        self.assertEqual(self.client.get(reverse('news_detail', args=['new-filters'])).status_code, 200)
        self.assertEqual(self.client.get(reverse('part_detail', args=[self.part.pk])).status_code, 200)

    def test_review_create_requires_login_and_saves_for_user(self):
        self.assertEqual(self.client.get(reverse('review_create')).status_code, 302)
        self.client.login(username='client', password='client12345')
        response = self.client.post(reverse('review_create'), {'rating': 5, 'text': 'Очень помогли с подбором детали.'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(text='Очень помогли с подбором детали.').exists())

    @patch('shop.views._safe_api_get')
    def test_external_api_page_uses_two_values(self, mocked_api):
        mocked_api.side_effect = [{'fact': 'Fact'}, {'ip': '127.0.0.1'}]
        response = self.client.get(reverse('external_apis'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fact')
        self.assertContains(response, '127.0.0.1')

    def test_stats_and_chart_for_logged_user(self):
        Sale.objects.create(client=self.client_profile, part=self.part, employee=self.employee, quantity=1, unit_price=self.part.price)
        self.client.login(username='client', password='client12345')
        self.assertEqual(self.client.get(reverse('stats')).status_code, 200)
        chart = self.client.get(reverse('sales_chart'))
        self.assertEqual(chart.status_code, 200)
        self.assertEqual(chart['Content-Type'], 'image/png')

# Create your tests here.
