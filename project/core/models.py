from django.db import models

# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Table(models.Model):
    name = models.CharField(max_length=30, unique=True)
    capacity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    class StatusChoice(models.TextChoices):
        PREPARING= 'p', 'Preparing'
        SERVED = 's', 'Served'
        READY = 'r', 'Ready'
    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    total = models.DecimalField()
    status = models.CharField(max_length=1, choices=StatusChoice, default=StatusChoice.PREPARING)

    def __str__(self):
        return f"{self.table}-{self.status}"

class OrderItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField()

    def __str__(self):
        return f"{self.menu_item}*{self.quantity}= {self.total}"