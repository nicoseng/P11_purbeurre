from django.core.management.base import BaseCommand
from purbeurre_website.category_importer import CategoryImporter
from purbeurre_website.product_importer import ProductImporter
from purbeurre_website.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):

        # Categories insertion
        if Category.objects.count() == 0:
            category_imported = CategoryImporter()
            category_url_json = category_imported.load_category_from_OFF()
            category_list = category_imported.extract_category(category_url_json, 30)
            category_imported.inject_category_in_database(category_list)
            self.stdout.write("Categories OFF bien importées.")

        else:
            self.stdout.write("Categories OFF déjà importées.")

        # Products insertion
        category_table = Category.objects.all()

        if Product.objects.count() == 0:

            product_imported = ProductImporter()
            products_list = product_imported.extract_products(category_table, 20)
            product_imported.inject_product_in_database(products_list, category_table)

            self.stdout.write("Produits OFF bien importées.")
        else:
            self.stdout.write("Produits OFF déjà importées.")
