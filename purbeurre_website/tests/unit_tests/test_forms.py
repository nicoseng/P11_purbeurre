from django.test import TestCase
from purbeurre_website.forms import CreateUser


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
