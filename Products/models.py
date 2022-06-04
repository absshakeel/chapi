from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from authentication.models import *
from django.urls import reverse

'''
categories model
'''
class Categories(models.Model):
    category_name=models.CharField(max_length=100, null=False, blank=False)
    slug=models.SlugField()
    image=models.ImageField(upload_to='categories', blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category_code=models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name

class Sub_Categories(models.Model):
    category = models.ForeignKey(
        Categories, 
        on_delete=models.CASCADE, 
        related_name='categories'
        )
    sub_category_name=models.CharField(max_length=100, null=False, blank=False)
    slug=models.SlugField()
    image=models.ImageField(upload_to='sub_categories', blank=True)
   
    description=models.TextField(max_length=1500, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.sub_category_name


'''
Brand model
'''
class Brand(models.Model):
    name = models.CharField(max_length=255,unique=True)
    brand_website = models.CharField(max_length=255,unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=False,)
    updated_at = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return self.name


'''
Countries model
'''
class Countreies(models.Model):
    # product = models.ManyToManyField(Products)
    name = models.CharField(max_length=255,unique=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


'''
product model
'''
class Products(models.Model):
    brand = models.ForeignKey(
        Brand, 
        on_delete=models.CASCADE,
        related_name= 'brand'
        )
    country = models.ForeignKey(Countreies,on_delete=models.CASCADE)
    category = models.ManyToManyField(Categories)
    sub_category = models.ManyToManyField(Sub_Categories)

    name = models.CharField(max_length=50, null=False, blank=False)
    slug = models.CharField(max_length=250, null=False, blank=False)
    meta = models.TextField(max_length=500, null=True, blank=True)
    descriptions = models.TextField(max_length=500, null=True, blank=True)
    alter_text = models.CharField(max_length=100, null=True, blank=True)

    feature_image=models.ImageField(upload_to='products')

    regular_price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    selling_price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)

    is_active= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    # def get_absolute_url(self):
    #     return reverse('product', kwargs={'pk': self.pk, 'slug':self.slug})

class Product_images(models.Model):
    product = models.ForeignKey(
        Products, 
        on_delete=models.CASCADE, 
        related_name='product_image'
        )
    image=models.ImageField(upload_to='product_image_gallery', blank=True)
    
    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")

'''
discount model
'''

class discount(models.Model):
    product = models.OneToOneField(Products, on_delete=models.CASCADE)
    discount_price = models.FloatField(default=0.00)
    discount_percent = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True,editable=False,)
    updated_at = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return self.product.name 


'''
coupon model 
''' 
class cupon(models.Model):
    product = models.OneToOneField(Products, on_delete=models.CASCADE)
    cupon_code = models.CharField(max_length=100)
    cupon_price = models.FloatField(default=0.00)
    cupon_discount = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True,editable=False,)
    updated_at = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return self.product.name

'''
Supplier model
'''
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=255)
    email = models.EmailField(
        blank=True,
        null = True,
        )
    phone = models.CharField(max_length=16)
    price = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    description = models.TextField(max_length=500)
    address = models.TextField(blank=False,null=False)

    created_at = models.DateTimeField(auto_now_add=True,editable=False,)
    updated_at = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return self.supplier_name
    
    class Meta:
        verbose_name = _("Supplier_name")
        verbose_name_plural = _("Supplier's")


'''
product attributes 
inventory model

'''

class ProductAttribute(models.Model):
    name = models.CharField(max_length=255,unique=False)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=255,unique=True,)
    product_type_attributes = models.ManyToManyField(
        ProductAttribute,
        related_name="product_type_attributes",
        through="ProductTypeAttribute"
        )

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="product_attribute",
        on_delete=models.PROTECT
        )
    attribute_value = models.CharField(max_length=255,)


class ProductInventory(models.Model):
    discount = models.OneToOneField(discount, on_delete=models.CASCADE)
    cupon = models.OneToOneField(cupon, on_delete=models.CASCADE)
    product_type = models.ForeignKey(
        ProductType, 
        related_name="product_type", 
        on_delete=models.PROTECT)
    product = models.ForeignKey(Products, related_name="product", on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,blank=True,null=True,)
    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        related_name="product_attribute_values",
        through="ProductAttributeValues"
        )

    sku = models.CharField(max_length=20,unique=True,)
    upc = models.CharField(max_length=12,unique=True,)

    is_active = models.BooleanField(default=False,)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    store_price = models.DecimalField(max_digits=10,decimal_places=2,)
   
    created_at = models.DateTimeField(auto_now_add=True,editable=False,)
    updated_at = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return self.sku


class ProductAttributeValues(models.Model):
    attributevalues = models.ForeignKey(
        "ProductAttributeValue",
        related_name="attributevaluess",
        on_delete=models.PROTECT
        )
    productinventory = models.ForeignKey(
        ProductInventory,
        related_name="productattributevaluess",
        on_delete=models.PROTECT
        )

    class Meta:
        unique_together = (("attributevalues", "productinventory"),)


class ProductTypeAttribute(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="productattribute",
        on_delete=models.PROTECT
        )
    product_type = models.ForeignKey(
        ProductType,
        related_name="producttype",
        on_delete=models.PROTECT
        )

    class Meta:
        unique_together = (("product_attribute", "product_type"),)

'''
 stock model
 '''
class Stock(models.Model):
    product_inventory = models.OneToOneField(
        ProductInventory,
        related_name="product_inventory",
        on_delete=models.PROTECT
        )
    last_checked = models.DateTimeField(null=True,blank=True,)
    units = models.IntegerField(default=0,)
    units_sold = models.IntegerField(default=0,)



'''
Cart model
'''
class Cart(models.Model):
    customer = models.ForeignKey(Profile,on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    complete = models.BooleanField(default=False)

    created_at = models.DateField(auto_now_add=True)

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ManyToManyField(Products)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    
    def __str__(self):
        return f"Cart=={self.cart.id}<==>CartProduct:{self.id}==Qualtity=={self.quantity}"


'''
Order model
'''
ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

class Order(models.Model):
    cart  = models.OneToOneField(Cart,on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=16)
    email = models.CharField(max_length=200)
    total = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    order_status = models.CharField(
        max_length=100,
        choices=ORDER_STATUS,
        default="Order Received"
        )
    date = models.DateField(auto_now_add=True)
    payment_complete = models.BooleanField(default=False,blank=True, null=True)

