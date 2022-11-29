from django.core.management.base import BaseCommand
from purbeurre_website.category_importer import CategoryImporter
from purbeurre_website.product_importer import ProductImporter
from purbeurre_website.models import Category, Product


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.category_imported = CategoryImporter()
        self.product_imported = ProductImporter()
        self.category_url_json = self.category_imported.load_category_from_OFF()
        self.category_list = self.category_imported.extract_category(self.category_url_json, 30)
        self.category_table = Category.objects.all()
        self.products_list = self.product_imported.extract_products(self.category_table, 20)
        self.product_table = Product.objects.all()

    def handle(self, *args, **options):

        # Categories insertion
        if Category.objects.count() == 0:
            self.category_imported.inject_category_in_database(self.category_list)
            self.stdout.write("Categories OFF bien importées.")

        else:
            if len(self.category_list) == Category.objects.count():
                self.stdout.write("La table catégorie est déjà mise à jour.")

            else:
                Category.objects.all().delete()
                self.category_imported.inject_category_in_database(self.category_list)
                self.stdout.write("Mise à jour des catégories effectuée.")

        # Products insertion
        if Product.objects.count() == 0:
            self.product_imported.inject_product_in_database(self.products_list, self.category_table)
            self.stdout.write("Produits OFF bien importées.")

        else:
            if len(self.products_list) == Product.objects.count():
                self.stdout.write("La table Produit est déjà mise à jour.")

            else:
                Product.objects.all().delete()
                self.product_imported.inject_product_in_database(self.products_list, self.category_table)
                self.stdout.write("Mise à jour des produits effectuée.")
