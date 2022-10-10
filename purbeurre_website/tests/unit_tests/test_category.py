from django.test import TestCase
from purbeurre_website.category_importer import CategoryImporter
from purbeurre_website.models import Category


class TestCategory(TestCase):

    def setUp(self):
        self.category_importer = CategoryImporter()
        self.test_category_list = [{"category_name": "Fruits",
                                    "category_url": "https://fr.openfoodfacts.org/categorie/fruits?json=1"},
                                   {"category_name": "Légumes",
                                    "category_url": "https://fr.openfoodfacts.org/categorie/legumes?json=1"}]

    def test_load_category_from_OFF(self):
        cat_imp = CategoryImporter()
        category_url_json = cat_imp.load_category_from_OFF()
        category_fetched = cat_imp.fetch_category(category_url_json, 2)

        expected_results = [
            {"category_name": "Aliments et boissons à base de végétaux",
             "category_url": "https://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux"},
            {"category_name": "Aliments d'origine végétale",
             "category_url": "https://fr.openfoodfacts.org/categorie/aliments-d-origine-vegetale"},
        ]
        assert expected_results == category_fetched

    def test_inject_category_in_database(self):

        test_results = self.category_importer.inject_category_in_database(self.test_category_list)

        num_id = 1
        nb_of_category = len(self.test_category_list)
        while num_id < nb_of_category:
            for category in self.test_category_list:
                category_data = Category(
                    category_id=num_id,
                    category_name=category["category_name"],
                    category_url=category["category_url"]
                )
                category_data.save()
                num_id = num_id + 1

        expected_results = Category.objects.all()
        assert len(test_results) == len(expected_results)

    def test_should_return_paginate_category_url(self):
        test_category_list = [{'category_name': 'Aliments et boissons à base de végétaux',
                               'category_url': 'https://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de'
                                               '-vegetaux'}]

        test_category_imported = CategoryImporter()
        test_paginate_category_url = test_category_imported.paginate_category_url(test_category_list, 1)
        expected_category_url_list = [
            'https://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux&page=0']
        assert test_paginate_category_url == expected_category_url_list

    def test_should_return_category_table_empty(self):
        test_category_imported = CategoryImporter()
        test_category_table = test_category_imported.category_table

        expected_category_table = Category.objects.all()
        self.assertQuerysetEqual(test_category_table, map(repr, expected_category_table))
