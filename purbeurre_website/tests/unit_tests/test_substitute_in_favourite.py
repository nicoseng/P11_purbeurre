from django.contrib.auth.models import User
from django.test import TestCase

from purbeurre_website.models import Product, Category, Favourite
from purbeurre_website.substitute_in_favourite import SubstituteInFavourite


class TestDeleteSubstitute(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            id=1,
            username="Lucie",
            email="lucie@gmail.com"
        )

        self.category = Category.objects.create(
            category_id=1,
            category_name="Fruits",
            category_url="https://fr.openfoodfacts.org/categorie/fruits?json=1"
        )
        self.product = Product.objects.create(
            category_id=Category(self.category.category_id),
            product_id=1,
            product_name="orange",
            product_image="https://images.openfoodf…/0397/front_fr.4.200.jpg",
            product_url="https://fr.openfoodfacts…anges-a-dessert-marque-u",
            product_ingredients="orange",
            product_nutriscore="a"
        )

    def test_inject_substitute_in_favourite(self):
        substitute_selected_data = {
            "product_name": "orange",
            "product_image": "https://images.openfoodf…/0397/front_fr.4.200.jpg",
            "product_nutriscore": "a"
        }

        Favourite.objects.create(
            user_id=User.objects.get(id=self.user.id),
            substitute_name="orange",
            substitute_image="https://images.openfoodf…/0397/front_fr.4.200.jpg",
            substitute_nutriscore="a"
        )
        test_favourite_database = Favourite.objects.all()
        subs_in_fav = SubstituteInFavourite()
        fav_db = subs_in_fav.inject_substitute_in_favourite(substitute_selected_data, self.user.id)
        assert len(test_favourite_database) == len(fav_db)

    def test_retrieve_favourite_database(self):
        Favourite.objects.create(
            user_id=User.objects.get(id=self.user.id),
            substitute_name="orange",
            substitute_image="https://images.openfoodf…/0397/front_fr.4.200.jpg",
            substitute_nutriscore="a"
        )
        test_favourite_database = Favourite.objects.all()
        subs_in_fav = SubstituteInFavourite()
        fav_db = subs_in_fav.retrieve_favourite_database(self.user.id)
        assert len(test_favourite_database) == len(fav_db)

    def test_inject_substitute_in_favourite(self):

        substitute_selected_data = {
            "product_name": "orange",
            "product_image": "https://images.openfoodf…/0397/front_fr.4.200.jpg",
            "product_nutriscore": "a"
        }

        Favourite.objects.create(
            user_id=User.objects.get(id=self.user.id),
            substitute_name="orange",
            substitute_image="https://images.openfoodf…/0397/front_fr.4.200.jpg",
            substitute_nutriscore="a"
        )
        test_favourite_database = Favourite.objects.all()
        subs_in_fav = SubstituteInFavourite()
        fav_db = subs_in_fav.inject_substitute_in_favourite(substitute_selected_data, self.user.id)
        assert len(test_favourite_database) == len(fav_db)
    #
    # def test_inject_substitute_in_favourite_2(self):
    #
    #     substitute_selected_data = {
    #         "product_name": "kitkat",
    #         "product_image": "https://images.openfoodf…/0397/front_fr.4.200.jpg",
    #         "nutriscore": "e"
    #     }
    #
    #     Favourite.objects.create(
    #         user_id=User.objects.get(id=self.user.id),
    #         substitute_name="orange",
    #         substitute_image="https://images.openfoodf…/0397/front_fr.4.200.jpg",
    #         substitute_nutriscore="a"
    #     )
    #     test_favourite_database = Favourite.objects.all()
    #     subs_in_fav = SubstituteInFavourite()
    #     fav_db = subs_in_fav.inject_substitute_in_favourite(substitute_selected_data, self.user.id)
    #     assert len(test_favourite_database) == len(fav_db)
