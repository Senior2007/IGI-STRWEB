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
    Supply,
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

    def test_registration_form_rejects_invalid_email(self):
        form = RegistrationForm(
            data={
                'username': 'new_client2',
                'first_name': 'Иван',
                'last_name': 'Петров',
                'birth_date': '1999-01-01',
                'phone': '+375 (29) 123-45-67',
                'email': 'not-an-email',
                'address': 'Минск',
                'password1': 'StrongPass12345',
                'password2': 'StrongPass12345',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


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
        promo = PromoCode.objects.create(
            code='TEST10',
            description='Тестовая скидка.',
            discount_percent=10,
            starts_at=date(2026, 1, 1),
            ends_at=date(2026, 12, 31),
        )
        promo.product_types.add(self.product_type)

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

    def test_user_without_client_redirected_to_complete_profile_on_buy(self):
        orphan = User.objects.create_user('orphan', password='orphan12345', first_name='О', last_name='Сиротин')
        self.client.login(username='orphan', password='orphan12345')
        response = self.client.get(reverse('sale_create'))
        self.assertRedirects(response, reverse('complete_client_profile'))

    def test_complete_client_profile_allows_purchase(self):
        orphan = User.objects.create_user('buyer2', password='buyer12345', email='buyer2@example.com')
        self.client.login(username='buyer2', password='buyer12345')
        response = self.client.post(
            reverse('complete_client_profile'),
            {
                'first_name': 'Покупатель',
                'last_name': 'Новый',
                'birth_date': '1995-06-06',
                'phone': '+375 (29) 888-77-66',
                'email': 'buyer2@example.com',
                'address': 'Минск',
            },
        )
        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(Client.objects.filter(user__username='buyer2').exists())
        response = self.client.post(reverse('sale_create'), {'part': self.part.pk, 'quantity': 1})
        self.assertEqual(response.status_code, 302)

    def test_registration_post_succeeds_with_csrf(self):
        session = self.client.session
        session.save()
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse('register'),
            {
                'username': 'newbuyer',
                'first_name': 'Новый',
                'last_name': 'Покупатель',
                'birth_date': '1995-05-05',
                'phone': '+375 (29) 555-66-77',
                'email': 'newbuyer@example.com',
                'address': 'Минск',
                'password1': 'StrongPass12345',
                'password2': 'StrongPass12345',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Client.objects.filter(user__username='newbuyer').exists())

    def test_sale_with_valid_promo_applies_discount(self):
        self.client.login(username='client', password='client12345')
        response = self.client.post(
            reverse('sale_create'),
            {'part': self.part.pk, 'quantity': 1, 'promo_code': 'TEST10'},
        )
        self.assertEqual(response.status_code, 302)
        sale = Sale.objects.latest('sold_at')
        self.assertEqual(sale.unit_price, Decimal('45.00'))

    def test_sale_rejects_promo_for_wrong_product_type(self):
        brakes_type = ProductType.objects.create(name='Тормозная система')
        promo = PromoCode.objects.create(
            code='BRAKEONLY',
            description='Только тормоза.',
            discount_percent=10,
            starts_at=date(2026, 1, 1),
            ends_at=date(2026, 12, 31),
        )
        promo.product_types.add(brakes_type)
        self.client.login(username='client', password='client12345')
        response = self.client.post(
            reverse('sale_create'),
            {'part': self.part.pk, 'quantity': 1, 'promo_code': 'BRAKEONLY'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Sale.objects.count(), 0)
        self.assertContains(response, 'не действует для типа')

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
        ]
        for name in url_names:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_promos_require_login(self):
        self.assertEqual(self.client.get(reverse('promos')).status_code, 302)
        self.client.login(username='client', password='client12345')
        self.assertEqual(self.client.get(reverse('promos')).status_code, 200)

    def test_part_list_filter_by_type(self):
        optics = ProductType.objects.create(name='Оптика')
        Part.objects.create(
            sku='T-OPT',
            name='Фара',
            product_type=optics,
            manufacturer=self.manufacturer,
            price=Decimal('100.00'),
            quantity=3,
            description='Тестовая оптика',
        )
        response = self.client.get(reverse('part_list'), {'type': optics.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Фара')
        self.assertNotContains(response, f'href="{self.part.get_absolute_url()}"')

    def test_part_list_search_without_javascript(self):
        response = self.client.get(reverse('part_list'), {'q': 'Фильтр'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Фильтр')
        self.assertNotContains(response, '<script>')

    def test_part_list_sort_by_price(self):
        cheap = Part.objects.create(
            sku='T-CHEAP',
            name='Дешевый',
            product_type=self.product_type,
            manufacturer=self.manufacturer,
            price=Decimal('10.00'),
            quantity=1,
            description='Дешевый товар',
        )
        expensive = Part.objects.create(
            sku='T-EXP',
            name='Дорогой',
            product_type=self.product_type,
            manufacturer=self.manufacturer,
            price=Decimal('999.00'),
            quantity=1,
            description='Дорогой товар',
        )
        response = self.client.get(reverse('part_list'), {'sort': 'price'})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertLess(content.index('Дешевый'), content.index('Дорогой'))
        response = self.client.get(reverse('part_list'), {'sort': 'price_desc'})
        content = response.content.decode()
        self.assertLess(content.index('Дорогой'), content.index('Дешевый'))

    def test_sku_hidden_for_regular_user(self):
        response = self.client.get(reverse('part_list'))
        self.assertNotContains(response, 'T-1')
        self.assertNotContains(response, '>Артикул<')
        response = self.client.get(reverse('part_detail', args=[self.part.pk]))
        self.assertNotContains(response, 'T-1')

    def test_sku_visible_for_staff(self):
        staff = User.objects.create_user('staff2', password='staff12345', is_staff=True)
        self.client.force_login(staff)
        response = self.client.get(reverse('part_list'))
        self.assertContains(response, 'T-1')
        self.assertContains(response, 'Артикул')

    def test_suppliers_hidden_for_regular_user(self):
        Supply.objects.create(
            supplier=self.supplier,
            part=self.part,
            quantity=10,
            unit_price=Decimal('30.00'),
        )
        response = self.client.get(reverse('part_detail', args=[self.part.pk]))
        self.assertNotContains(response, 'Поставщик')
        self.assertNotContains(response, '>Поставщики<')
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'поставщиков')

    def test_suppliers_visible_for_staff(self):
        Supply.objects.create(
            supplier=self.supplier,
            part=self.part,
            quantity=10,
            unit_price=Decimal('30.00'),
        )
        staff = User.objects.create_user('staff3', password='staff12345', is_staff=True)
        self.client.force_login(staff)
        response = self.client.get(reverse('part_detail', args=[self.part.pk]))
        self.assertContains(response, 'Поставщик')
        self.assertContains(response, 'Поставщики')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'поставщиков')

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

    def test_stats_and_chart_for_staff_only(self):
        Sale.objects.create(client=self.client_profile, part=self.part, employee=self.employee, quantity=1, unit_price=self.part.price)
        self.client.login(username='client', password='client12345')
        self.assertEqual(self.client.get(reverse('stats')).status_code, 302)
        self.assertEqual(self.client.get(reverse('sales_chart')).status_code, 302)

        staff = User.objects.create_user('stats_staff', password='staff12345', is_staff=True)
        self.client.force_login(staff)
        self.assertEqual(self.client.get(reverse('stats')).status_code, 200)
        chart = self.client.get(reverse('sales_chart'))
        self.assertEqual(chart.status_code, 200)
        self.assertEqual(chart['Content-Type'], 'image/png')

# Create your tests here.
