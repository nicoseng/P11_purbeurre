from django.core.management.base import BaseCommand
from purbeurre_website.product_importer import ProductImporter
from purbeurre_website.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Products insertion
        category_table = Category.objects.all()
        print(category_table)
        print("Voici le nombre de produits contenus dans votre table produits :", Product.objects.count())

        if Product.objects.count() == 0:

            product_imported = ProductImporter()
            products_list = product_imported.extract_products(category_table, 2)
            print('Products_list:\n', products_list)
            product_imported.inject_product_in_database(products_list, category_table)
            self.stdout.write("Produits OFF bien importées.")

        else:
            self.stdout.write("Produits OFF déjà importées.")
