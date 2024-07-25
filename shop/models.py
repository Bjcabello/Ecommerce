from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')
    description = RichTextField(verbose_name='Descripción')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    stock = models.IntegerField(verbose_name='Inventario')
    image = models.CharField(max_length=4000, verbose_name='Imagen', null=True, blank=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    products = models.ManyToManyField(Product, through='OrderProduct', verbose_name='Productos')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending', verbose_name='Estado')

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Órdenes'

    def __str__(self):
        return f"Orden {self.id} - {self.date}"

    def get_total_price(self):
        return sum(order_product.quantity * order_product.product.price for order_product in self.orderproduct_set.all())

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Orden')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    quantity = models.IntegerField(verbose_name='Cantidad', default=1)

    class Meta:
        verbose_name = 'Producto de la Orden'
        verbose_name_plural = 'Productos de la Orden'

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
