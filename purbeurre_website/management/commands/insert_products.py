from django.core.management.base import BaseCommand
from purbeurre_website.product_importer import ProductImporter
from purbeurre_website.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_database = Category.objects.all()
        if len(Product.objects.all()) == 0:

            try:
                product_imported = ProductImporter()
                category_url_list = product_imported.load_category_url()
                products_list = product_imported.extract_products(category_url_list, 20)
                product_imported.inject_product_in_database(products_list, category_database)

            except:
                Product.objects.all()
            self.stdout.write("Produits OFF bien importées.")

        else:
            self.stdout.write("Produits OFF déjà importées.")
