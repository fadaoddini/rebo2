from django.db import models

from catalogue.models import Product
from login.models import MyUser


class Bid(models.Model):
    OK = True
    NO = False

    RESULT_BID = (
        (OK, 'OK'),
        (NO, 'NO'),
    )
    product = models.ForeignKey(Product, related_name='bids', on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField()
    weight = models.PositiveBigIntegerField(blank=True, null=True, default=0)
    user = models.ForeignKey(MyUser, related_name='bids', on_delete=models.RESTRICT)
    result = models.BooleanField(choices=RESULT_BID, default=OK)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Bid'
        verbose_name_plural = "Bids"

    @classmethod
    def add_bid(cls, request, upc):
        result = "200"
        result1 = False
        form = request.POST
        user = request.user
        price = form.get('price')
        weight = form.get('weight')
        if price:
            price = int(price)
        else:
            result = "20"
            return result
        product = Product.objects.filter(upc=upc).first()

        exist_bid = Bid.objects.filter(user=user).filter(product=product).first()

        if exist_bid:
            exist_bid.price = price
            exist_bid.weight = weight
            exist_bid.save()
            result = "400"
        else:

            new_bid = Bid(user=user, product=product, price=price, weight=weight, result=result1)
            new_bid.save()
            result = "100"
        return result

    @classmethod
    def ok_bid(cls, request, pk):
        result = "200"
        form = request.POST
        user = request.user
        bid = Bid.objects.filter(pk=pk).first()
        bid.result = True
        bid.save()
        result = "100"
        return result

    @classmethod
    def no_bid(cls, request, pk):
        result = "200"
        form = request.POST
        user = request.user
        bid = Bid.objects.filter(pk=pk).first()
        bid.result = False
        bid.save()
        result = "100"
        return result
