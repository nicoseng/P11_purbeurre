from django.core.management.base import BaseCommand
from purbeurre_website.category_importer import CategoryImporter
from purbeurre_website.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):

        if len(Category.objects.all()) == 0:

            try:
                category_imported = CategoryImporter()
                category_url_json = category_imported.load_category_from_OFF()
                category_list = category_imported.fetch_category(category_url_json, 20)
                category_imported.inject_category_in_database(category_list)
                category_imported.paginate_category_url(category_list)

            except:
                Category.objects.all()
            self.stdout.write("Categories OFF bien importées.")

        else:
            self.stdout.write("Categories OFF déjà importées.")
