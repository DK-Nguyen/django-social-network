from django.test import TestCase
from django.db import models
from django.core.exceptions import FieldDoesNotExist

from users.models import SiteUser
from users.forms import UserRegisterForm, UserUpdateForm


# Create your tests here.
class SiteUserTest(TestCase):
    fixtures = ['testusers.json']

    def _testFieldType(self, model, modelname, fieldname, type):
        try:
            field = model._meta.get_field(fieldname)
            self.assertTrue(isinstance(field, type),
                            "Testing the type of %s field in model %s" % (fieldname, modelname))
        except FieldDoesNotExist:
            self.assertTrue(False, "Testing if field %s exists in model %s" % (fieldname, modelname))
        return field

    def testFieldTypes(self):
        self._testFieldType(SiteUser, 'SiteUser', 'first_name', models.CharField)
        self._testFieldType(SiteUser, 'SiteUser', 'last_name', models.CharField)
        self._testFieldType(SiteUser, 'SiteUser', 'email', models.EmailField)
        self._testFieldType(SiteUser, 'SiteUser', 'email_verified', models.BooleanField)
        self._testFieldType(SiteUser, 'SiteUser', 'phone_number', models.CharField)
        self._testFieldType(SiteUser, 'SiteUser', 'address', models.TextField)
        self._testFieldType(SiteUser, 'SiteUser', 'bio', models.TextField)
        self._testFieldType(SiteUser, 'SiteUser', 'profile_picture', models.ImageField)


class TestUserUpdateForm(TestCase):
    fixtures = [ 'testusers.json' ]

    valid_data = {
        'first_name': 'Hai',
        'last_name': 'Luong',
        'phone_number': '0123456789',
        'address': 'Wonderland',
        'bio': 'A new bio'
    }

    def testValidForm(self):
        form = UserUpdateForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), "Testing if valid form data is really valid")

    def _createInvalidFieldData(self, field):
        temp_data = self.valid_data.copy()
        temp_data[field] = ''
        return temp_data

    def testEmptyFieldForm(self):
        empty_first_name_form = UserUpdateForm(data=self._createInvalidFieldData('first_name'))
        self.assertFalse(empty_first_name_form.is_valid())
        empty_last_name_form = UserUpdateForm(data=self._createInvalidFieldData('last_name'))
        self.assertFalse(empty_last_name_form.is_valid())
        empty_phone_number_form = UserUpdateForm(data=self._createInvalidFieldData('phone_number'))
        self.assertFalse(empty_phone_number_form.is_valid())
        empty_address_form = UserUpdateForm(data=self._createInvalidFieldData('phone_number'))
        self.assertFalse(empty_address_form.is_valid())


class TestUserRegisterForm(TestCase):
    fixtures = [ 'testusers.json' ]

    valid_data = {
        'username': 'hailuong',
        'password1': '12345678abc',
        'password2': '12345678abc',
        'first_name': 'Hai',
        'last_name': 'Luong',
        'email': 'luong@example.com',
        'phone_number': '0123456789',
        'address': 'Wonderland',
        'bio': ''
    }

    def testValidForm(self):
        form = UserRegisterForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), "Testing if valid form data is really valid")

    def _createInvalidFieldData(self, field):
        temp_data = self.valid_data.copy()
        temp_data[field] = ''
        return temp_data

    def testEmptyFieldForm(self):
        # We don't test empty username, password and password2 since the base form of django already make it reliable
        empty_first_name_form = UserRegisterForm(data=self._createInvalidFieldData('first_name'))
        self.assertFalse(empty_first_name_form.is_valid())
        empty_last_name_form = UserRegisterForm(data=self._createInvalidFieldData('last_name'))
        self.assertFalse(empty_last_name_form.is_valid())
        empty_email_form = UserRegisterForm(data=self._createInvalidFieldData('email'))
        self.assertFalse(empty_email_form.is_valid())
        empty_phone_number_form = UserRegisterForm(data=self._createInvalidFieldData('phone_number'))
        self.assertFalse(empty_phone_number_form.is_valid())
        empty_address_form = UserRegisterForm(data=self._createInvalidFieldData('phone_number'))
        self.assertFalse(empty_address_form.is_valid())

    def testSameEmailForm(self):
        same_email_form_data = self.valid_data.copy()
        same_email_form_data['email'] = 'testuser@example.com' # email from fixture
        form = UserRegisterForm(data=same_email_form_data)
        self.assertFalse(form.is_valid())

