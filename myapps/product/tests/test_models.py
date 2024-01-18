from django.test import TestCase
from models import *
from django.core.exceptions import ValidationError,IntegrityError
from django.db import models

class ModelTest(TestCase):
    def setUp(self):
        
        self.user1 = CustomUser.objects.create_user(
            email="user1@example.com",
            password="user1",
            first_name="User",
            last_name="One",
            phonenumber="+989111111111",
            username="asdd"
        )
        self.user2 = CustomUser.objects.create_user(
            email="user2@example.com",
            password="user2",
            first_name="User",
            last_name="Two",
            phonenumber="+989222222222",
            username="asd"
        )
        
        self.detail1 = Detail.objects.create(title="Books", parent=None, is_deleted=False, created_at="2021-01-01", creator=self.user1)
        self.detail2 = Detail.objects.create(title="Fiction", parent=self.detail1, is_deleted=False, created_at="2021-01-02", creator=self.user2)
        
        self.product1 = Product.objects.create(title="Harry Potter", description="A fantasy novel", detail_id=self.detail2, count=10, price=100.0, is_deleted=False, created_at="2021-01-01", creator=self.user1)
        self.product2 = Product.objects.create(title="Lord of the Rings", description="An epic novel", detail_id=self.detail2, count=20, price=200.0, is_deleted=False, created_at="2021-01-02", creator=self.user2)
       
        self.comment1 = Comment.objects.create(content="I love this book", is_ok=True, parent=None, item_id=self.product1, is_deleted=False, created_at="2021-01-01", creator=self.user1)
        self.comment2 = Comment.objects.create(content="Me too", is_ok=True, parent=self.comment1, item_id=self.product1, is_deleted=False, created_at="2021-01-02", creator=self.user2)
        
        self.discount1 = DicountPercent.objects.create(expiration="2021-01-31", percent=0.1, product_id=self.product1, is_deleted=False, created_at="2021-01-01", creator=self.user1)
        self.discount2 = DicountPercent.objects.create(expiration="2021-01-31", percent=0.2, product_id=self.product2, is_deleted=False, created_at="2021-01-02", creator=self.user2)

    def test_status_creator_type(self):
        
        
        self.assertTrue(isinstance(self.product1.creator, models.ForeignKey))
        self.assertTrue(isinstance(self.comment1.creator, models.ForeignKey))

    def test_status_created_at_type(self):
        
        self.assertTrue(isinstance(self.comment1.created_at, models.DateTimeField))
        self.assertTrue(isinstance(self.product1.created_at, models.DateTimeField))

    def test_status_is_deleted_type(self):
       
        self.assertTrue(isinstance(self.product1.is_deleted, models.BooleanField))
        self.assertTrue(isinstance(self.comment1.is_deleted, models.BooleanField))

    def test_detail_title_type(self):
       
     
        self.assertTrue(isinstance(self.detail1.title, models.CharField))
        self.assertTrue(isinstance(self.detail2.title, models.CharField))

    def test_detail_title_max_length(self):
        
        self.assertEqual(len(self.detail1.title), 50)
        self.assertEqual(len(self.detail2.title), 50)

    def test_detail_title_unique(self):
        
        self.assertTrue(self.detail1._meta.get_field('title').unique)
        self.assertTrue(self.detail2._meta.get_field('title').unique)

    def test_detail_parent_type(self):
        
        self.assertTrue(isinstance(self.detail1.parent, models.ForeignKey))
        self.assertTrue(isinstance(self.detail2.parent, models.ForeignKey))

    def test_product_title_type(self):
        
        self.assertTrue(isinstance(self.product1.title, models.CharField))
        self.assertTrue(isinstance(self.product2.title, models.CharField))

    def test_product_title_max_length(self):
        
        self.assertEqual(len(self.product1.title), 50)
        self.assertEqual(len(self.product2.title), 50)

    def test_product_description_type(self):
        
        self.assertTrue(isinstance(self.product1.description, models.CharField))
        self.assertTrue(isinstance(self.product2.description, models.CharField))

    def test_product_description_max_length(self):
        
        self.assertEqual(len(self.product1.description), 500)
        self.assertEqual(len(self.product2.description), 500)

    def test_product_detail_id_type(self):
        
       
        self.assertTrue(isinstance(self.product1.detail_id, models.ManyToManyField))
        self.assertTrue(isinstance(self.product2.detail_id, models.ManyToManyField))

    def test_product_count_type(self):
       
        self.assertTrue(isinstance(self.product1.count, models.PositiveIntegerField))
        self.assertTrue(isinstance(self.product2.count, models.PositiveIntegerField))

    def test_product_price_type(self):
       
        self.assertTrue(isinstance(self.product1.price, models.FloatField))
        self.assertTrue(isinstance(self.product2.price, models.FloatField))

    def test_product_price_validator(self):
       
        self.product1.clean_price()
        self.product2.clean_price()
        
        with self.assertRaises(ValidationError):
            self.product1.price = -10.0
            self.product1.clean_price()
        with self.assertRaises(ValidationError):
            self.product2.price = 10000.0
            self.product2.clean_price()

    def test_comment_content_type(self):
        
        self.assertTrue(isinstance(self.comment1.content, models.TextField))
        self.assertTrue(isinstance(self.comment2.content, models.TextField))

    def test_comment_content_max_length(self):
       
        self.assertEqual(len(self.comment1.content), 600)
        self.assertEqual(len(self.comment2.content), 600)

    def test_comment_is_ok_type(self):
        
        self.assertTrue(isinstance(self.comment1.is_ok, models.BooleanField))
        self.assertTrue(isinstance(self.comment2.is_ok, models.BooleanField))

    def test_comment_parent_type(self):
        self.assertTrue(isinstance(self.comment2.parent, models.ForeignKey))

    def test_product_title_unique(self):
        
        with self.assertRaises(IntegrityError):
            Product.objects.create(title="Harry Potter", description="A book about Python", count=20, price=200.0)