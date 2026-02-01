from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" с необходимыми правами'

    def handle(self, *args, **options):
        product_content_type = ContentType.objects.get_for_model(Product)

        group, created = Group.objects.get_or_create(name="Модератор продуктов")

        # Права
        perms = [
            Permission.objects.get(codename="can_unpublish_product", content_type=product_content_type),
            Permission.objects.get(codename="delete_product", content_type=product_content_type),
        ]

        group.permissions.set(perms)
        self.stdout.write(
            self.style.SUCCESS('Группа "Модератор продуктов" успешно настроена')
        )
