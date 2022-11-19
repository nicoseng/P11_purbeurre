from django.test import TestCase
from purbeurre_website.category_importer import CategoryImporter
from purbeurre_website.models import Category


class TestCategory(TestCase):

    def setUp(self):
        self.category_importer = CategoryImporter()
        self.test_category_list = [{"name": "Fruits",
                                    "url": "https://fr.openfoodfacts.org/categorie/fruits?json=1"},
                                   {"name": "Légumes",
                                    "url": "https://fr.openfoodfacts.org/categorie/legumes?json=1"}]

    def test_extract_category(self):
        category_url_json = self.category_importer = CategoryImporter().load_category_from_OFF()
        category_list = self.category_importer = CategoryImporter().extract_category(category_url_json, 2)
        expected_results = [
            {
                'name': category_list[0]["name"],
                'url': category_list[0]["url"],
            },
            {
                'name': category_list[1]["name"],
                'url': category_list[1]["url"]
            }
        ]
        assert expected_results == category_list

    def test_inject_category_in_database(self):
        Category.objects.bulk_create([
            Category(
                category_id=1,
                category_name="Fruits",
                category_url="https://fr.openfoodfacts.org/categorie/fruits?json=1"
            ),
            Category(
                category_id=2,
                category_name="Légumes",
                category_url="https://fr.openfoodfacts.org/categorie/legumes?json=1"
            )
        ])
        test_results = self.category_importer.inject_category_in_database(self.test_category_list)
        expected_results = Category.objects.all()
        assert len(test_results) == len(expected_results)
