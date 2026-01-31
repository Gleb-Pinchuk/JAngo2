from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Удаляет все данные и добавляет тестовые категории и продукты'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Все данные удалены.'))

        electronics = Category.objects.create(
            name="Электроника",
            description="Гаджеты и техника"
        )
        books = Category.objects.create(
            name="Книги",
            description="Художественная литература"
        )

        Product.objects.create(
            name="Ноутбук",
            description="Мощный игровой ноутбук",
            category=electronics,
            price=1200.00
        )
        Product.objects.create(
            name="Смартфон",
            description="Флагманский смартфон",
            category=electronics,
            price=800.00
        )
        Product.objects.create(
            name="Роман",
            description="Бестселлер этого года",
            category=books,
            price=15.99
        )

        self.stdout.write(
            self.style.SUCCESS('Тестовые данные успешно добавлены!')
        )
