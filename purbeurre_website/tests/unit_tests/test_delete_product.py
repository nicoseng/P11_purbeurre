from django.contrib.auth.models import User
from django.test import TestCase

from purbeurre_website.delete_product import ProductEliminator
from purbeurre_website.models import Favourite


class TestDeleteSubstitute(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            id=1,
            username="Lucie",
            email="lucie@gmail.com"
        )
        self.fav_db = Favourite.objects.all()
        self.subs_in_fav = Favourite.objects.create(
            # user_id=self.user.id,
            substitute_id=1,
            substitute_name="orange",
            substitute_image="https://images.openfoodf…/0397/front_fr.4.200.jpg",
            substitute_nutriscore="a"
        )

    def test_delete_substitute(self):
        prod_eliminator = ProductEliminator()
        print(self.subs_in_fav.substitute_id)
        fav_db_fetched = prod_eliminator.delete_substitute(self.subs_in_fav.substitute_id)
        assert len(fav_db_fetched) == 0
