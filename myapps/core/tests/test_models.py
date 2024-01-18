from django.test import TestCase
from ..models import *
from ...product.models import Product
from ...member.models import CustomUser
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.models import ContentType

class ModelTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            email="user1@example.com",
            password="user1",
            firstname="User",
            lastname="One",
            phone="+989111111111",
            username="asd"
        )
        self.user2 = CustomUser.objects.create_user(
            email="user2@example.com",
            password="user2",
            firstname="User",
            lastname="Two",
            phone="+989222222222",
            username="asdd"
        )
       
        self.product1 = Product.objects.create(title="Book", description="A book about Django", count=10, price=100.0, is_deleted=False, created_at="2021-01-01", creator=self.user1)
        self.product2 = Product.objects.create(title="Pen", description="A pen for writing", count=20, price=50.0, is_deleted=False, created_at="2021-01-02", creator=self.user2)
        
        self.like1 = Like.objects.create(content_type=ContentType.objects.get_for_model(Product), object_id=self.product1.id, is_deleted=False, created_at="2021-01-01", creator=self.user1)
        self.like2 = Like.objects.create(content_type=ContentType.objects.get_for_model(Product), object_id=self.product2.id, is_deleted=False, created_at="2021-01-02", creator=self.user2)
       
        self.image1 = Image.objects.create(content_type=ContentType.objects.get_for_model(Product), object_id=self.product1.id, image="book.jpg", is_deleted=False, created_at="2021-01-01", creator=self.user1)
        self.image2 = Image.objects.create(content_type=ContentType.objects.get_for_model(Product), object_id=self.product2.id, image="pen.jpg", is_deleted=False, created_at="2021-01-02", creator=self.user2)
       
        self.edites1 = Edites.objects.create(content_type=ContentType.objects.get_for_model(Product), object_id=self.product1.id, field_changed="price", old_value="100.0", is_deleted=False, created_at="2021-01-01", creator=self.user1)
        self.edites2 = Edites.objects.create(content_type=ContentType.objects.get_for_model(Product), object_id=self.product2.id, field_changed="count", old_value="20", is_deleted=False, created_at="2021-01-02", creator=self.user2)

    def test_like_content_type_type(self):
        self.assertIs(self.like1.content_type.__class__, models.ForeignKey)
        # self.assertTrue(isinstance(self.like1.content_type, models.ForeignKey))
        # self.assertTrue(isinstance(self.like2.content_type, models.ForeignKey))

    def test_like_object_id_type(self):
        
        self.assertTrue(isinstance(self.like1.object_id, models.PositiveIntegerField))
        self.assertTrue(isinstance(self.like2.object_id, models.PositiveIntegerField))

    def test_like_content_object_type(self):
        
        self.assertTrue(isinstance(self.like1.content_object, GenericForeignKey))
        self.assertTrue(isinstance(self.like2.content_object, GenericForeignKey))

    def test_image_content_type_type(self):
       
        
        self.assertTrue(isinstance(self.image1.content_type, models.ForeignKey))
        self.assertTrue(isinstance(self.image2.content_type, models.ForeignKey))

    def test_image_object_id_type(self):
       
        self.assertTrue(isinstance(self.image1.object_id, models.PositiveIntegerField))
        self.assertTrue(isinstance(self.image2.object_id, models.PositiveIntegerField))

    def test_image_content_object_type(self):
        
        self.assertTrue(isinstance(self.image1.content_object, GenericForeignKey))
        self.assertTrue(isinstance(self.image2.content_object, GenericForeignKey))

    def test_image_image_type(self):
       
        self.assertTrue(isinstance(self.image1.image, models.ImageField))
        self.assertTrue(isinstance(self.image2.image, models.ImageField))

    def test_image_image_path(self):
        
        self.assertEqual(self.image1.image.path, os.path.join('images','product', 'book.jpg'))
        self.assertEqual(self.image2.image.path, os.path.join('images','product', 'pen.jpg'))

    def test_edites_content_type_type(self):
       
        self.assertTrue(isinstance(self.edites1.content_type, models.ForeignKey))
        self.assertTrue(isinstance(self.edites2.content_type, models.ForeignKey))

    def test_edites_object_id_type(self):
       
        self.assertTrue(isinstance(self.edites1.object_id, models.PositiveIntegerField))
        self.assertTrue(isinstance(self.edites2.object_id, models.PositiveIntegerField))

    def test_edites_content_object_type(self):
        
        self.assertTrue(isinstance(self.edites1.content_object, GenericForeignKey))
        self.assertTrue(isinstance(self.edites2.content_object, GenericForeignKey))

    def test_edites_field_changed_type(self):
        
        self.assertTrue(isinstance(self.edites1.field_changed, models.CharField))
        self.assertTrue(isinstance(self.edites2.field_changed, models.CharField))

    def test_edites_field_changed_max_length(self):
        
        self.assertEqual(len(self.edites1.field_changed), 100)
        self.assertEqual(len(self.edites2.field_changed), 100)

    def test_edites_old_value_type(self):
       
        self.assertTrue(isinstance(self.edites1.old_value, models.CharField))
        self.assertTrue(isinstance(self.edites2.old_value, models.CharField))

    def test_edites_old_value_max_length(self):
        
        self.assertEqual(len(self.edites1.old_value), 100)
        self.assertEqual(len(self.edites2.old_value), 100)
