from django.db import models
from authapp.models import User
from mainapp.models import Product
# Create your models here.


# Creating the manager for the working with the whole QuerySet:
class BasketQuerySet(models.QuerySet):

    def delete(self):
        for item in self:
            item.product.quantity += item.quantity
            item.product.save()
        super().delete()


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()  # Redefined field "objects" to work with the QuerySet

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in baskets)

    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.sum() for basket in baskets)

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

    # Option 1 on to work with remaining goods with functions:
    # def delete(self, *args, **kwargs):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete(*args, **kwargs)
    #
    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.__class__.objects.get(pk=self.pk).quantity  # Deal with difference of products in base and in the Basket
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super().save(*args, **kwargs)



    #  Option 2 Deal with product quantity with signals: in ordersapp/view

