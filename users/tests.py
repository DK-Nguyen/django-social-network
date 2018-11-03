from django.test import TestCase

from .forms import UserUpdateForm

# Create your tests here.
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
        # We don't test empty username, password and password2 since the base form of django already make it reliable
        empty_first_name_form = UserUpdateForm(data=self._createInvalidFieldData('first_name'))
        self.assertFalse(empty_first_name_form.is_valid())
        empty_last_name_form = UserUpdateForm(data=self._createInvalidFieldData('last_name'))
        self.assertFalse(empty_last_name_form.is_valid())
        empty_phone_number_form = UserUpdateForm(data=self._createInvalidFieldData('phone_number'))
        self.assertFalse(empty_phone_number_form.is_valid())
        empty_address_form = UserUpdateForm(data=self._createInvalidFieldData('phone_number'))
        self.assertFalse(empty_address_form.is_valid())
