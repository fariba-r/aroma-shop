from django.test import TestCase
from ..models import Province, City,CustomUser,UserAddress
from django.core.validators import RegexValidator, validate_email
from django.core.exceptions import ValidationError

class CityProvinceTest(TestCase):
    def setUp(self):
        # create some provinces
        self.province1 = Province.objects.create(name="Tehran")
        self.province2 = Province.objects.create(name="Isfahan")
        # create some cities
        self.city1 = City.objects.create(name="Tehran", province_id=self.province1)
        self.city2 = City.objects.create(name="Karaj", province_id=self.province1)
        self.city3 = City.objects.create(name="Isfahan", province_id=self.province2)
        self.city4 = City.objects.create(name="Kashan", province_id=self.province2)

    def test_province_name(self):
        # test the name attribute of the province model
        self.assertEqual(self.province1.name, "Tehran")
        self.assertEqual(self.province2.name, "Isfahan")

    def test_city_name(self):
        # test the name attribute of the city model
        self.assertEqual(self.city1.name, "Tehran")
        self.assertEqual(self.city2.name, "Karaj")
        self.assertEqual(self.city3.name, "Isfahan")
        self.assertEqual(self.city4.name, "Kashan")

    def test_city_province_id(self):
        # test the province_id attribute of the city model
        self.assertEqual(self.city1.province_id, self.province1)
        self.assertEqual(self.city2.province_id, self.province1)
        self.assertEqual(self.city3.province_id, self.province2)
        self.assertEqual(self.city4.province_id, self.province2)

    def test_province_related_name(self):
        # test the related_name attribute of the province model
        self.assertEqual(self.province1.province.all().count(), 2)
        self.assertEqual(self.province2.province.all().count(), 2)
        self.assertIn(self.city1, self.province1.province.all())
        self.assertIn(self.city2, self.province1.province.all())
        self.assertIn(self.city3, self.province2.province.all())
        self.assertIn(self.city4, self.province2.province.all())

class CustomUserTest(TestCase):
    def setUp(self):
        # create some custom users
        self.user1 = CustomUser.objects.create_user(
            email="user1@example.com",
            password="user1",
            first_name="User",
            last_name="One",
            phonenumber="+989111111111",
            username="asd"
        )
        self.user2 = CustomUser.objects.create_user(
            email="user2@example.com",
            password="user2",
            first_name="User",
            last_name="Two",
            phonenumber="+989222222222",
            username="ashd"
        )

    def test_custom_user_email(self):
        # test the email attribute of the custom user model
        self.assertEqual(self.user1.email, "user1@example.com")
        self.assertEqual(self.user2.email, "user2@example.com")

    def test_custom_user_password(self):
        # test the password attribute of the custom user model
        self.assertTrue(self.user1.check_password("user1"))
        self.assertTrue(self.user2.check_password("user2"))

    def test_custom_user_name(self):
        # test the first_name and last_name attributes of the custom user model
        self.assertEqual(self.user1.first_name, "User")
        self.assertEqual(self.user1.last_name, "One")
        self.assertEqual(self.user2.first_name, "User")
        self.assertEqual(self.user2.last_name, "Two")

    def test_custom_user_phonenumber(self):
        # test the phonenumber attribute of the custom user model
        self.assertEqual(self.user1.phonenumber, "+989111111111")
        self.assertEqual(self.user2.phonenumber, "+989222222222")

    def test_custom_user_status(self):
        # test the is_deleted and created_at attributes of the custom user model
        self.assertFalse(self.user1.is_deleted)
        self.assertFalse(self.user2.is_deleted)
        self.assertIsNotNone(self.user1.created_at)
        self.assertIsNotNone(self.user2.created_at)


    def test_custom_user_phonenumber_validator(self):
        
        validator = RegexValidator(regex=r'^(?:\+98|0)?9[0-9]{2}(?:0-9{2}|[0-9]{8})$', message="Invalid phonenumber number format. Example: +989123456789 or 09123456789")
       
        validator(self.user1.phonenumber)
        validator(self.user2.phonenumber)
     
        with self.assertRaises(ValidationError):
            validator("1234567890")
        with self.assertRaises(ValidationError):
            validator("+9891234567890")

    def test_custom_user_email_validator(self):
        
       
        validate_email(self.user1.email)
        validate_email(self.user2.email)
        
        with self.assertRaises(ValidationError):
            validate_email("user@example")
        with self.assertRaises(ValidationError):
            validate_email("user@example.com.com")

    def test_custom_user_phonenumber_max_length(self):
        
        self.assertEqual(len(self.user1.phonenumber), 50)
        self.assertEqual(len(self.user2.phonenumber), 50)

    def test_custom_user_email_max_length(self):
        
        self.assertEqual(len(self.user1.email), 80)
        self.assertEqual(len(self.user2.email), 80)

    def test_custom_user_password_max_length(self):
       
        self.assertEqual(len(self.user1.password), 200)
        self.assertEqual(len(self.user2.password), 200)

    