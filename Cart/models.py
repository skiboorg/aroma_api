from django.db import models




class Cart(models.Model):
    session_id = models.CharField(max_length=255, null=True, blank=True,)
    user = models.ForeignKey('user.User',on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField(default=0)

    # def save(self, *args, **kwargs):
    #
    #
    #     super().save(*args, **kwargs)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True, related_name='items')
    item = models.ForeignKey('Item.Item', on_delete=models.CASCADE, blank=True, null=True)
    volume = models.ForeignKey('Item.ItemVolume', on_delete=models.CASCADE, blank=True, null=True)
    box = models.CharField('Упаковка', max_length=20, blank=True, null=True)
    amount = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.price = self.volume.price * self.amount
        self.cart.price += self.price
        self.cart.save()
        super().save(*args, **kwargs)
