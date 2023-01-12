from django.test import TestCase
from purbeurre_website.forms import CreateUser, ChangePasswordForm, UpdateUserForm
from purbeurre_website.models import Product, Category, User
from purbeurre_website.product_importer import ProductImporter


class TestForms(TestCase):

    def test_create_user_form_valid_data(self):
        form = CreateUser(data={
            'username': 'nicolas',
            'email': 'nicolas.abc@gmail.com',
            'password1': 'molaires',
            'password2': 'molaires'
        })
        self.assertTrue(form.is_valid())

    def test_create_user_form_no_valid_data_1(self):
        form = CreateUser(data={
            'username': 'nicolas',
            'email': 'nicolas.abcgmail.com',
            'password1': '&*$',
            'password2': 'z&1235'
        })
        self.assertFalse(form.is_valid())

    def test_create_user_form_no_valid_data_2(self):
        form = CreateUser(data={
            'username': 2456,
            'email': 'nicolas.com',
            'password1': '&*$',
            'password2': 'z&1235'
        })
        self.assertFalse(form.is_valid())

    def test_create_user_form_no_data(self):
        form = CreateUser(data={})
        self.assertFalse(form.is_valid())

    def test_update_user_form_valid_data(self):

        test_update_user = UpdateUserForm(data={
            'new_username': "abc",
            'new_email': 'abc@gmail.com'
        })
        self.assertTrue(test_update_user.is_valid())

    def test_update_user(self):
        self.user = User.objects.create(
            id=4,
            username="mdr",
            email="mdr@gmail.com",
            password="lunaires"
        )
        update_user_form = UpdateUserForm(data={
            'new_username': "abc",
            'new_email': 'abc@gmail.com',
            'password': 'lunaires'
        })
        new_username = update_user_form["new_username"].value()
        new_email = update_user_form["new_email"].value()
        update_user_form.update_user(self.user, new_username, new_email, self.user.password)
        expected_new_username = "abc"
        expected_new_email = "abc@gmail.com"
        assert new_username == expected_new_username
        assert new_email == expected_new_email

    def test_change_password(self):
        self.user = User.objects.create(
            id=4,
            username="mdr",
            email="mdr@gmail.com",
            password="lunaires"
        )

        change_password_form = ChangePasswordForm(self.user.username, data={
            'new_password1': "solaires",
            'new_password2': 'solaires'
        })

        new_password1 = change_password_form["new_password1"].value()
        new_password2 = change_password_form["new_password2"].value()
        expected_new_password1 = "solaires"
        expected_new_password2 = "solaires"
        assert new_password1 == expected_new_password1
        assert new_password2 == expected_new_password2
        self.assertTrue(change_password_form.is_valid())

    def test_change_password_no_valid(self):
        self.user = User.objects.create(
            id=4,
            username="mdr",
            email="mdr@gmail.com",
            password="lunaires"
        )

        change_password_form = ChangePasswordForm(self.user.username, data={
            'new_password1': "solaires",
            'new_password2': 'molaires'
        })

        new_password1 = change_password_form["new_password1"].value()
        new_password2 = change_password_form["new_password2"].value()
        expected_new_password1 = "solaires"
        expected_new_password2 = "molaires"
        assert new_password1 == expected_new_password1
        assert new_password2 == expected_new_password2
        self.assertFalse(change_password_form.is_valid())
