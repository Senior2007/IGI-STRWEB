from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from shop.models import (
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
)


class Command(BaseCommand):
    help = 'Заполняет демонстрационные данные для лабораторной работы.'

    def handle(self, *args, **options):
        self._clear_domain_data()
        admin = self._user('admin', 'admin12345', 'Администратор', 'Системный', is_staff=True, is_superuser=True)
        staff_user = self._user('manager', 'manager12345', 'Андрей', 'Ковалев', is_staff=True)

        company_items = [
            (2016, 'Открытие магазина', 'Компания начала работу с розничных продаж расходников для популярных марок авто.', 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?auto=format&fit=crop&w=900&q=80'),
            (2017, 'Первый склад', 'Запущен складской учет поставок, остатков и резервов под клиентские заказы.', 'https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc?auto=format&fit=crop&w=900&q=80'),
            (2018, 'Поставщики из ЕС', 'Подключены прямые поставки фильтров, тормозных систем и ремней ГРМ.', 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=900&q=80'),
            (2019, 'Онлайн-каталог', 'Каталог стал доступен клиентам с поиском по артикулу, типу детали и изготовителю.', 'https://images.unsplash.com/photo-1517048676732-d65bc937f952?auto=format&fit=crop&w=900&q=80'),
            (2020, 'Сервис подбора', 'Менеджеры начали подбирать запчасти по VIN и истории обслуживания автомобиля.', 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=900&q=80'),
            (2021, 'Контроль качества', 'Каждая партия проходит сверку документов, упаковки и маркировки изготовителя.', 'https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?auto=format&fit=crop&w=900&q=80'),
            (2022, 'B2B-направление', 'Добавлены условия для СТО: резервирование складских позиций и постоплата.', 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=900&q=80'),
            (2023, 'Расширение ассортимента', 'В каталоге появились элементы подвески, датчики, оптика и кузовные детали.', 'https://images.unsplash.com/photo-1565043666747-69f6646db940?auto=format&fit=crop&w=900&q=80'),
            (2024, 'Складская аналитика', 'Продажи и остатки анализируются по типам товаров, поставщикам и сезонности.', 'https://images.unsplash.com/photo-1553413077-190dd305871c?auto=format&fit=crop&w=900&q=80'),
            (2025, 'Доставка по Беларуси', 'Запущена отправка заказов по регионам с отслеживанием статуса комплектации.', 'https://images.unsplash.com/photo-1501700493788-fa1a4fc9fe62?auto=format&fit=crop&w=900&q=80'),
        ]
        for year, title, content, logo_url in company_items:
            CompanyInfo.objects.create(year=year, title=title, content=content, logo_url=logo_url)

        news_items = [
            ('fresh-brake-discs', 'Новые тормозные диски Brembo уже на складе', 'Поступила партия дисков для Volkswagen, Audi и Skoda.', 'Партия прошла проверку по артикулам и сертификатам. Для клиентов действует резерв на 48 часов после оформления заявки.', 'https://images.unsplash.com/photo-1603386329225-868f9b1ee6c9?auto=format&fit=crop&w=900&q=80'),
            ('winter-filters', 'Подготовили зимний набор фильтров', 'В каталог добавлены воздушные и салонные фильтры для зимнего обслуживания.', 'Комплекты подобраны под самые частые модели клиентов и доступны в рознице и для СТО.', 'https://images.unsplash.com/photo-1517524008697-84bbe3c3fd98?auto=format&fit=crop&w=900&q=80'),
            ('battery-sensors', 'Расширили раздел датчиков и электрики', 'На складе появились датчики ABS, кислородные датчики и реле.', 'Новые позиции добавлены с привязкой к изготовителям и поставщикам, чтобы менеджеры быстрее проверяли совместимость.', 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=900&q=80'),
            ('oil-promo', 'Акция на моторные масла 5W-30', 'До конца месяца действует скидка на популярные масла для бензиновых двигателей.', 'Промокоды доступны в личном кабинете и на странице купонов.', 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=900&q=80'),
            ('warehouse-inventory', 'Завершена инвентаризация склада', 'Остатки синхронизированы с каталогом и доступны для поиска.', 'После инвентаризации обновлены количества и даты последних поставок.', 'https://images.unsplash.com/photo-1587293852726-70cdb56c2866?auto=format&fit=crop&w=900&q=80'),
            ('suspension-week', 'Неделя деталей подвески', 'Рычаги, стойки стабилизатора и сайлентблоки выделены в отдельную подборку.', 'Менеджеры подготовили таблицу совместимости для распространенных моделей автомобилей.', 'https://images.unsplash.com/photo-1565043666747-69f6646db940?auto=format&fit=crop&w=900&q=80'),
            ('new-supplier-ngk', 'Подключен поставщик свечей NGK', 'Ассортимент свечей зажигания стал шире на 34 позиции.', 'Поставки идут через проверенный канал, данные по партиям занесены в складской учет.', 'https://images.unsplash.com/photo-1597852074816-d933c7d2b988?auto=format&fit=crop&w=900&q=80'),
            ('optics-update', 'Обновлен раздел автомобильной оптики', 'Добавлены фары, противотуманные лампы и корректоры света.', 'Каждая позиция получила фото, описание и данные изготовителя.', 'https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=900&q=80'),
            ('delivery-regions', 'Доставка заказов теперь доступна по регионам', 'Отправляем оплаченные заказы транспортными службами по Беларуси.', 'Клиент видит покупку в личном кабинете, а менеджер контролирует продажу в админке.', 'https://images.unsplash.com/photo-1570129477492-45c003edd2be?auto=format&fit=crop&w=900&q=80'),
            ('summer-cooling', 'Сезонная подборка по системе охлаждения', 'Радиаторы, термостаты и антифризы вынесены в отдельную витрину.', 'Подборка помогает заранее подготовить автомобиль к летним поездкам.', 'https://images.unsplash.com/photo-1542362567-b07e54358753?auto=format&fit=crop&w=900&q=80'),
        ]
        for index, (slug, title, summary, content, image_url) in enumerate(news_items):
            NewsArticle.objects.create(
                slug=slug,
                title=title,
                summary=summary,
                content=content,
                image_url=image_url,
                published_at=timezone.now() - timedelta(days=9 - index),
            )

        terms = [
            ('Артикул', 'Уникальный код детали, по которому поставщик и магазин идентифицируют товар.'),
            ('VIN-подбор', 'Поиск детали по идентификационному номеру автомобиля.'),
            ('Оригинальная деталь', 'Запчасть, поставляемая под брендом производителя автомобиля.'),
            ('Аналог', 'Совместимая деталь стороннего изготовителя.'),
            ('Складской остаток', 'Фактическое количество товара, доступное для продажи.'),
            ('Поставка', 'Факт закупки товара у поставщика с количеством, датой и закупочной ценой.'),
            ('Резерв', 'Временное удержание товара под заказ клиента.'),
            ('Расходники', 'Детали и материалы для регулярного обслуживания автомобиля.'),
            ('Кросс-номер', 'Альтернативный артикул совместимой детали.'),
            ('Гарантийный срок', 'Период, в течение которого можно предъявить претензию по качеству товара.'),
        ]
        for index, (title, definition) in enumerate(terms, start=1):
            Term.objects.create(title=title, definition=definition, added_on=date(2026, 5, index))

        vacancies = [
            ('Менеджер по подбору запчастей', 'Консультации клиентов, подбор деталей по каталогу и VIN.', 1500, 2300, True),
            ('Специалист склада', 'Приемка поставок, маркировка и контроль остатков.', 1300, 1900, True),
            ('Оператор интернет-заказов', 'Обработка заявок сайта и согласование самовывоза.', 1200, 1700, True),
            ('B2B-менеджер для СТО', 'Работа с корпоративными клиентами и регулярными поставками.', 1800, 2600, True),
            ('Закупщик автозапчастей', 'Переговоры с поставщиками и контроль закупочных цен.', 1700, 2500, True),
            ('Контент-специалист каталога', 'Фото, описания, характеристики и проверка карточек товаров.', 1200, 1800, True),
            ('Курьер по Минску', 'Доставка мелких заказов и документов клиентам.', 1100, 1600, True),
            ('Бухгалтер по первичке', 'Накладные, акты сверки и учет оплат.', 1500, 2200, False),
            ('Маркетолог промоакций', 'Промокоды, рассылки и анализ спроса.', 1600, 2400, False),
            ('Системный администратор', 'Поддержка рабочих мест и локальной сети магазина.', 1700, 2500, False),
        ]
        for title, description, salary_min, salary_max, is_active in vacancies:
            Vacancy.objects.create(
                title=title,
                description=description,
                salary_min=Decimal(salary_min),
                salary_max=Decimal(salary_max),
                is_active=is_active,
            )

        types = {
            name: ProductType.objects.create(name=name, description=description)
            for name, description in [
                ('Фильтры', 'Масляные, воздушные, топливные и салонные фильтры.'),
                ('Тормозная система', 'Диски, колодки, жидкости и датчики износа.'),
                ('Подвеска', 'Амортизаторы, рычаги, стойки и сайлентблоки.'),
                ('Электрика', 'Датчики, реле, лампы и элементы проводки.'),
                ('Масла и жидкости', 'Моторные масла, антифриз, тормозная жидкость.'),
                ('Ремни и ролики', 'Комплекты ГРМ, приводные ремни и натяжители.'),
                ('Свечи зажигания', 'Свечи для бензиновых двигателей разных типоразмеров.'),
                ('Кузовные детали', 'Зеркала, крепления, молдинги и элементы защиты.'),
                ('Оптика', 'Фары, лампы, противотуманки и корректоры света.'),
                ('Двигатель', 'Прокладки, термостаты, помпы и датчики двигателя.'),
            ]
        }

        manufacturers = {
            name: Manufacturer.objects.create(name=name, country=country, website=website)
            for name, country, website in [
                ('Bosch', 'Germany', 'https://www.boschaftermarket.com/'),
                ('Brembo', 'Italy', 'https://www.brembo.com/'),
                ('Mann-Filter', 'Germany', 'https://www.mann-filter.com/'),
                ('KYB', 'Japan', 'https://www.kyb.com/'),
                ('NGK', 'Japan', 'https://www.ngkntk.com/'),
                ('Valeo', 'France', 'https://www.valeo.com/'),
                ('Gates', 'USA', 'https://www.gates.com/'),
                ('Febi Bilstein', 'Germany', 'https://partsfinder.bilsteingroup.com/'),
                ('Hella', 'Germany', 'https://www.hella.com/'),
                ('Mahle', 'Germany', 'https://www.mahle-aftermarket.com/'),
            ]
        }

        supplier_data = [
            ('АвтоЛогистик Минск', 'Минск, ул. Монтажников, 12', '+375 (29) 101-11-21', 'logistic@autoparts.test'),
            ('БелЗапчасть Плюс', 'Минск, ул. Машиностроителей, 7', '+375 (29) 102-12-22', 'belparts@autoparts.test'),
            ('EuroParts Trade', 'Брест, ул. Складская, 4', '+375 (29) 103-13-23', 'euro@autoparts.test'),
            ('JapanAuto Supply', 'Гродно, пр-т Космонавтов, 18', '+375 (29) 104-14-24', 'japan@autoparts.test'),
            ('СТО Комплект', 'Минск, ул. Автодоровская, 9', '+375 (29) 105-15-25', 'sto@autoparts.test'),
            ('MotorLine BY', 'Витебск, ул. Терешковой, 21', '+375 (29) 106-16-26', 'motorline@autoparts.test'),
            ('DriveMarket', 'Минск, ул. Промышленная, 33', '+375 (29) 107-17-27', 'drive@autoparts.test'),
            ('OpticCar', 'Могилев, ул. Первомайская, 55', '+375 (29) 108-18-28', 'optic@autoparts.test'),
            ('Garage Partner', 'Гомель, ул. Барыкина, 10', '+375 (29) 109-19-29', 'garage@autoparts.test'),
            ('RapidParts', 'Минск, ул. Радиальная, 40', '+375 (29) 110-20-30', 'rapid@autoparts.test'),
        ]
        suppliers = [Supplier.objects.create(name=name, address=address, phone=phone, email=email) for name, address, phone, email in supplier_data]

        part_data = [
            ('AP-FIL-184', 'Масляный фильтр Mann W 712/95', 'Фильтры', 'Mann-Filter', '32.90', 64, 'Фильтр для плановой замены масла, подходит для популярных бензиновых двигателей.', 'https://images.unsplash.com/photo-1607860108855-64acf2078ed9?auto=format&fit=crop&w=900&q=80'),
            ('AP-BRK-220', 'Тормозные колодки Brembo P 85 020', 'Тормозная система', 'Brembo', '118.50', 42, 'Передние колодки с низким уровнем шума и стабильным торможением.', 'https://images.unsplash.com/photo-1603386329225-868f9b1ee6c9?auto=format&fit=crop&w=900&q=80'),
            ('AP-SUS-314', 'Амортизатор KYB Excel-G', 'Подвеска', 'KYB', '207.00', 28, 'Газомасляный амортизатор для ежедневной эксплуатации и неровных дорог.', 'https://images.unsplash.com/photo-1565043666747-69f6646db940?auto=format&fit=crop&w=900&q=80'),
            ('AP-ELC-411', 'Датчик кислорода Bosch LSU', 'Электрика', 'Bosch', '164.20', 21, 'Лямбда-зонд для контроля состава смеси и корректной работы двигателя.', 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=900&q=80'),
            ('AP-OIL-530', 'Моторное масло 5W-30 синтетика', 'Масла и жидкости', 'Mahle', '74.00', 85, 'Синтетическое масло для бензиновых и дизельных двигателей с турбонаддувом.', 'https://images.unsplash.com/photo-1487754180451-c456f719a1fc?fm=jpg&q=80&w=900&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('AP-BLT-612', 'Комплект ремня ГРМ Gates PowerGrip', 'Ремни и ролики', 'Gates', '236.80', 19, 'Комплект ремня и роликов для регламентной замены газораспределительного механизма.', 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?auto=format&fit=crop&w=900&q=80'),
            ('AP-SPK-704', 'Свеча зажигания NGK Iridium IX', 'Свечи зажигания', 'NGK', '41.30', 96, 'Иридиевая свеча с устойчивой искрой и увеличенным ресурсом.', 'https://images.unsplash.com/photo-1597852074816-d933c7d2b988?auto=format&fit=crop&w=900&q=80'),
            ('AP-BDY-825', 'Корпус правого зеркала Febi', 'Кузовные детали', 'Febi Bilstein', '89.90', 17, 'Корпус наружного зеркала под окраску, поставляется с креплениями.', 'https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=900&q=80'),
            ('AP-LGT-912', 'Фара Hella Performance LED', 'Оптика', 'Hella', '312.40', 13, 'Светодиодная фара с четкой светотеневой границей и надежным корпусом.', 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=900&q=80'),
            ('AP-ENG-101', 'Термостат Valeo 87C', 'Двигатель', 'Valeo', '58.60', 37, 'Термостат системы охлаждения с уплотнительным кольцом в комплекте.', 'https://images.unsplash.com/photo-1542362567-b07e54358753?auto=format&fit=crop&w=900&q=80'),
        ]
        parts = []
        for index, (sku, name, type_name, manufacturer_name, price, quantity, description, image_url) in enumerate(part_data):
            part = Part.objects.create(
                sku=sku,
                name=name,
                product_type=types[type_name],
                manufacturer=manufacturers[manufacturer_name],
                price=Decimal(price),
                quantity=quantity,
                description=description,
                image_url=image_url,
            )
            parts.append(part)
            Supply.objects.create(
                supplier=suppliers[index],
                part=part,
                purchase_date=date(2026, 4, index + 1),
                quantity=25 + index * 3,
                unit_price=(Decimal(price) * Decimal('0.72')).quantize(Decimal('0.01')),
            )

        client_data = [
            ('client1', 'client12345', 'Илья', 'Мартынов', date(1994, 2, 14), '+375 (33) 201-21-31', 'ilya.martynov@example.com', 'Минск, ул. Гурского, 18'),
            ('client2', 'client12345', 'Анна', 'Савицкая', date(1991, 6, 3), '+375 (33) 202-22-32', 'anna.sav@example.com', 'Минск, ул. Немига, 6'),
            ('client3', 'client12345', 'Павел', 'Лисовский', date(1988, 9, 20), '+375 (33) 203-23-33', 'pavel.lis@example.com', 'Брест, ул. Московская, 44'),
            ('client4', 'client12345', 'Мария', 'Громова', date(1997, 11, 9), '+375 (33) 204-24-34', 'maria.gromova@example.com', 'Гродно, ул. Советская, 12'),
            ('client5', 'client12345', 'Денис', 'Руденко', date(1990, 4, 27), '+375 (33) 205-25-35', 'denis.rud@example.com', 'Гомель, ул. Кирова, 31'),
            ('client6', 'client12345', 'Ольга', 'Кравец', date(1986, 12, 5), '+375 (33) 206-26-36', 'olga.kravets@example.com', 'Витебск, ул. Ленина, 72'),
            ('client7', 'client12345', 'Никита', 'Баранов', date(1995, 7, 18), '+375 (33) 207-27-37', 'nikita.baranov@example.com', 'Минск, ул. Калиновского, 50'),
            ('client8', 'client12345', 'Елена', 'Мельник', date(1992, 3, 24), '+375 (33) 208-28-38', 'elena.melnik@example.com', 'Могилев, пр-т Мира, 16'),
            ('client9', 'client12345', 'Сергей', 'Орлов', date(1989, 8, 30), '+375 (33) 209-29-39', 'sergey.orlov@example.com', 'Минск, ул. Якуба Коласа, 21'),
            ('client10', 'client12345', 'Кристина', 'Демидова', date(1996, 5, 11), '+375 (33) 210-30-40', 'kristina.demidova@example.com', 'Бобруйск, ул. Минская, 8'),
        ]
        clients = []
        for username, password, first_name, last_name, birth_date, phone, email, address in client_data:
            user = self._user(username, password, first_name, last_name, email=email)
            clients.append(Client.objects.create(user=user, first_name=first_name, last_name=last_name, birth_date=birth_date, phone=phone, email=email, address=address))

        employee_data = [
            (staff_user, 'Андрей', 'Ковалев', 'Старший менеджер продаж', date(1987, 3, 12), '+375 (44) 301-31-41', 'andrey.kovalev@autoparts.test', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=900&q=80', 'Ведет крупных клиентов и контролирует сделки по поставкам для СТО.'),
            (None, 'Виктория', 'Нестерова', 'Менеджер интернет-заказов', date(1992, 8, 22), '+375 (44) 302-32-42', 'victoria.nesterova@autoparts.test', 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=900&q=80', 'Обрабатывает заявки сайта, подтверждает остатки и сроки самовывоза.'),
            (None, 'Роман', 'Тарасов', 'Специалист склада', date(1985, 1, 19), '+375 (44) 303-33-43', 'roman.tarasov@autoparts.test', 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=900&q=80', 'Принимает поставки, сверяет количество и маркировку деталей.'),
            (None, 'Дарья', 'Белая', 'Контент-специалист', date(1993, 4, 7), '+375 (44) 304-34-44', 'daria.belaya@autoparts.test', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=900&q=80', 'Добавляет фото, описания и характеристики товаров в каталог.'),
            (None, 'Максим', 'Жук', 'Закупщик', date(1989, 10, 15), '+375 (44) 305-35-45', 'maxim.zhuk@autoparts.test', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=900&q=80', 'Согласует закупочные цены и контролирует график поставок.'),
            (None, 'Татьяна', 'Соколова', 'B2B-менеджер', date(1984, 2, 26), '+375 (44) 306-36-46', 'tatiana.sokolova@autoparts.test', 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=900&q=80', 'Работает с автосервисами и корпоративными клиентами.'),
            (None, 'Егор', 'Миронов', 'Специалист по гарантии', date(1991, 9, 2), '+375 (44) 307-37-47', 'egor.mironov@autoparts.test', 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=900&q=80', 'Проверяет обращения по качеству и документы на возврат.'),
            (None, 'Наталья', 'Волкова', 'Бухгалтер', date(1986, 6, 17), '+375 (44) 308-38-48', 'natalia.volkova@autoparts.test', 'https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=900&q=80', 'Ведет первичные документы, оплаты и сверки с поставщиками.'),
            (None, 'Артем', 'Федоров', 'Курьер', date(1998, 12, 4), '+375 (44) 309-39-49', 'artem.fedorov@autoparts.test', 'https://images.unsplash.com/photo-1547425260-76bcadfb4f2c?auto=format&fit=crop&w=900&q=80', 'Доставляет срочные заказы по Минску и документы клиентам.'),
            (None, 'Инна', 'Петрова', 'Маркетолог', date(1990, 5, 29), '+375 (44) 310-40-50', 'inna.petrova@autoparts.test', 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=900&q=80', 'Готовит промокоды, новости и сезонные подборки товаров.'),
        ]
        employees = [
            Employee.objects.create(user=user, first_name=first_name, last_name=last_name, position=position, birth_date=birth_date, phone=phone, email=email, photo_url=photo_url, responsibilities=responsibilities)
            for user, first_name, last_name, position, birth_date, phone, email, photo_url, responsibilities in employee_data
        ]

        for index, part in enumerate(parts):
            Sale.objects.create(
                client=clients[index],
                part=part,
                employee=employees[index],
                sold_at=timezone.now() - timedelta(days=index),
                quantity=1 + index % 3,
                unit_price=part.price,
            )

        review_data = [
            ('Илья Мартынов', 5, 'Нашли фильтр по артикулу за пару минут, забрал в тот же день.'),
            ('Анна Савицкая', 4, 'Понравилось, что менеджер сразу сказал разницу между оригиналом и аналогом.'),
            ('Павел Лисовский', 5, 'Колодки пришли в нормальной упаковке, документы были на месте.'),
            ('Мария Громова', 5, 'Заказала лампы и салонный фильтр, все позиции совпали с описанием.'),
            ('Денис Руденко', 4, 'Хороший выбор по подвеске, но хотелось бы больше вариантов доставки вечером.'),
            ('Ольга Кравец', 5, 'Помогли подобрать масло и не пытались продать лишнее.'),
            ('Никита Баранов', 4, 'Удобный каталог, поиск по типам деталей действительно спасает время.'),
            ('Елена Мельник', 5, 'Сотрудник проверил совместимость датчика перед оплатой.'),
            ('Сергей Орлов', 5, 'Скидка по промокоду сработала, заказ отдали быстро.'),
            ('Кристина Демидова', 4, 'Все аккуратно, но страницу с доставкой стоит сделать подробнее.'),
        ]
        for index, (name, rating, text) in enumerate(review_data):
            Review.objects.create(user=clients[index].user, name=name, rating=rating, text=text)

        promo_data = [
            ('BRAKE15', 'Скидка на тормозные колодки и диски при заказе комплектом.', 15, date(2026, 5, 1), date(2026, 6, 15), True),
            ('FILTER10', 'Скидка на масляные, воздушные и салонные фильтры.', 10, date(2026, 5, 1), date(2026, 6, 10), True),
            ('OILWEEK', 'Специальная цена на моторные масла 5W-30.', 12, date(2026, 5, 5), date(2026, 6, 5), True),
            ('KYBPLUS', 'Скидка на амортизаторы KYB при покупке пары.', 8, date(2026, 5, 10), date(2026, 6, 20), True),
            ('LIGHT7', 'Скидка на лампы, фары и элементы автомобильной оптики.', 7, date(2026, 5, 1), date(2026, 5, 31), True),
            ('VINHELP', 'Бесплатная проверка совместимости по VIN для заказов от 100 BYN.', 5, date(2026, 5, 12), date(2026, 6, 12), True),
            ('STO20', 'B2B-скидка для автосервисов на складские позиции.', 20, date(2026, 5, 1), date(2026, 7, 1), True),
            ('SUMMERCOOL', 'Скидка на радиаторы, антифризы и термостаты.', 11, date(2026, 5, 15), date(2026, 6, 30), True),
            ('APRILPARTS', 'Архивная акция на весеннее обслуживание.', 9, date(2026, 4, 1), date(2026, 4, 30), False),
            ('OLDSTOCK', 'Архивный купон на распродажу старых складских остатков.', 18, date(2026, 3, 1), date(2026, 3, 31), False),
        ]
        promo_type_map = {
            'BRAKE15': ['Тормозная система'],
            'FILTER10': ['Фильтры'],
            'OILWEEK': ['Масла и жидкости'],
            'KYBPLUS': ['Подвеска'],
            'LIGHT7': ['Оптика'],
            'SUMMERCOOL': ['Двигатель', 'Масла и жидкости'],
            'APRILPARTS': ['Фильтры', 'Масла и жидкости'],
            'OLDSTOCK': [],
        }
        for code, description, discount, starts_at, ends_at, is_active in promo_data:
            promo = PromoCode.objects.create(
                code=code,
                description=description,
                discount_percent=discount,
                starts_at=starts_at,
                ends_at=ends_at,
                is_active=is_active,
            )
            type_names = promo_type_map.get(code)
            if type_names:
                promo.product_types.set(types[name] for name in type_names)

        oil_image_url = 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=900&q=80'
        broken_oil_image = 'https://images.unsplash.com/photo-1635437367037-9271d8b81f50?auto=format&fit=crop&w=900&q=80'
        Part.objects.filter(image_url=broken_oil_image).update(image_url=oil_image_url)
        NewsArticle.objects.filter(image_url=broken_oil_image).update(image_url=oil_image_url)

        self.stdout.write(self.style.SUCCESS('Демонстрационные данные созданы. admin/admin12345, manager/manager12345, client1/client12345.'))

    def _user(self, username, password, first_name, last_name, email='', is_staff=False, is_superuser=False):
        user, _ = User.objects.get_or_create(username=username)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save()
        return user

    def _clear_domain_data(self):
        for model in [Sale, Supply, Review, PromoCode, Part, Supplier, Manufacturer, ProductType, Client, Employee, Vacancy, Term, NewsArticle, CompanyInfo]:
            model.objects.all().delete()
