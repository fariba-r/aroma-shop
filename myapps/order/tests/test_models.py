from django.test import TestCase

from ...member.models import CustomUser,Staff
from django.core.exceptions import ValidationError
from django.db import models
from ...product.models import Product,Detail
from ..models import Order, ProductOrder, DiscountCodeUsed

from django.db import models

class DiscountCodeUsedTest(TestCase):
    def setUp(self):
        
        self.user1 = CustomUser.objects.create( 
            email="user1@example.com",
            password="user1",
            first_name="User",
            last_name="One",
            phonenumber="+989111111111",
            username="asd"

            )
        
        self.staff = Staff.objects.create(
            user_id=self.user1,
            expiration="2021-01-10",
            position="observer"
        )
        
        self.code1 = DiscountCodeUsed.objects.create(creator=self.staff, created_at="2021-01-01", value=10.0)
        self.code2 = DiscountCodeUsed.objects.create(creator=self.staff, created_at="2021-01-02", value=20.0)
        self.detail=Detail.objects.create(creator=self.staff, created_at="2021-01-02",title="green")
        self.product1 = Product.objects.create(title="Book", description="A book about Django", detail_id=self.detail, count=10, price=100.0)
        self.product2 = Product.objects.create(title="Pen", description="A pen for writing", detail_id=self.detail, count=20, price=50.0)
       
        self.code1 = DiscountCodeUsed.objects.create(creator=self.staff, created_at="2021-01-01", date_used="2021-01-01", value=10.0)
        self.code2 = DiscountCodeUsed.objects.create(creator=self.staff, created_at="2021-01-02", date_used="2021-01-02", value=20.0)
        
        
        
        self.product_order1 = ProductOrder.objects.create(product_id=self.product1, order_id=self.order1, count=1)
        self.product_order2 = ProductOrder.objects.create(product_id=self.product2, order_id=self.order2, count=2)

        self.order1 = Order.objects.create(product_id=self.product_order1, discount_code_id=self.code1, final_payment=90.0, pyment_status="P")
        self.order2 = Order.objects.create(product_id=self.product_order2, discount_code_id=self.code2, final_payment=80.0, pyment_status="D")

    def test_discount_code_used_value_validator(self):
        self.code1.validate_payment(self.code1.value)
        self.code2.validate_payment(self.code2.value)
        with self.assertRaises(ValidationError):
            self.code1.validate_payment(-10.0)

    def test_discount_code_used_creator_type(self):
        self.assertTrue(isinstance(self.code1.creator, models.ForeignKey))
        self.assertTrue(isinstance(self.code2.creator, models.ForeignKey))

    def test_discount_code_used_created_at_type(self):
        self.assertTrue(isinstance(self.code1.created_at, models.DateTimeField))
        self.assertTrue(isinstance(self.code2.created_at, models.DateTimeField))

    def test_discount_code_used_date_used_type(self):
        self.assertTrue(isinstance(self.code1.date_used, models.DateTimeField))
        self.assertTrue(isinstance(self.code2.date_used, models.DateTimeField))

    def test_discount_code_used_value_type(self):
        self.assertTrue(isinstance(self.code1.value, models.FloatField))
        self.assertTrue(isinstance(self.code2.value, models.FloatField))

    def test_discount_code_used_value_max_length(self):
        self.assertEqual(len(str(self.code1.value)), 4)
        self.assertEqual(len(str(self.code2.value)), 4)




        

    def test_order_product_id_type(self):
       
        self.assertTrue(isinstance(self.order1.product_id, models.ManyToManyField))
        self.assertTrue(isinstance(self.order2.product_id, models.ManyToManyField))

    def test_order_discount_code_id_type(self):
       
        self.assertTrue(isinstance(self.order1.discount_code_id, models.OneToOneField))
        self.assertTrue(isinstance(self.order2.discount_code_id, models.OneToOneField))

    def test_order_final_payment_type(self):
        
        self.assertTrue(isinstance(self.order1.final_payment, models.FloatField))
        self.assertTrue(isinstance(self.order2.final_payment, models.FloatField))

    def test_order_final_payment_validator(self):
        
        self.order1.validate_payment(self.order1.final_payment)
        self.order2.validate_payment(self.order2.final_payment)
       
        with self.assertRaises(ValidationError):
            self.order1.validate_payment(-10.0)

    def test_order_pyment_status_type(self):
       
        self.assertTrue(isinstance(self.order1.pyment_status, models.CharField))
        self.assertTrue(isinstance(self.order2.pyment_status, models.CharField))

    def test_order_pyment_status_max_length(self):
       
        self.assertEqual(len(self.order1.pyment_status), 1)
        self.assertEqual(len(self.order2.pyment_status), 1)

    def test_product_order_product_id_type(self):
       
        self.assertTrue(isinstance(self.product_order1.product_id, models.ForeignKey))
        self.assertTrue(isinstance(self.product_order2.product_id, models.ForeignKey))

    def test_product_order_order_id_type(self):
        
        self.assertTrue(isinstance(self.product_order1.order_id, models.ForeignKey))
        self.assertTrue(isinstance(self.product_order2.order_id, models.ForeignKey))

    def test_product_order_count_type(self):
       
        self.assertTrue(isinstance(self.product_order1.count, models.PositiveIntegerField))
        self.assertTrue(isinstance(self.product_order2.count, models.PositiveIntegerField))
