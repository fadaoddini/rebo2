from decimal import Decimal

from django.conf import settings
from shop import models


class Shipping:
    def __init__(self, request):
        self.session = request.session
        location = self.session.get(settings.ADDRESS_SHIPPING)
        if not location:
            location = self.session[settings.ADDRESS_SHIPPING] = {}
        self.location = location

    def add(self, location, location_count=1, update_location=False):
        location_id = str(location.id)
        if location_id not in self.location:
            self.location[location_id] = {
                                     'location_count': 0,
                                     'name': str(location.name),
                                     'family': str(location.family),
                                     'mobile': str(location.mobile),
                                     'address': str(location.address),
                                     'ostan': str(location.ostan),
                                     'shahr': str(location.shahr),
                                     'codeposti': str(location.codeposti)}
        if update_location:
            self.location[location_id]['location_count'] = location_count
            location_info = models.Location.objects.filter(id=location_id).first()
            user = location_info.user
            locations = models.Location.objects.filter(user=user).all()

            for address in locations:
                if address.id == int(location_id):
                    address.is_active = True
                    address.save()
                else:
                    address.is_active = False
                    address.save()

        else:
            self.location[location_id]['location_count'] = 0
        self.save()

    def save(self):
        self.session[settings.ADDRESS_SHIPPING] = self.location
        self.session.modified = True

    def show_address_choose(self):
        choose_location = ""
        location_ids = self.location.keys()
        addresses = models.Location.objects.filter(id__in=location_ids)
        for address in addresses:
            if address.is_active is True:
                self.location[str(address.id)]['location'] = address
                choose_location = address

        return choose_location


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, product_count=1, update_count=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'product_count': 0,
                                     'price': str(product.price),
                                     'discount': str(product.discount),
                                     'weight': str(product.weight)}
        if update_count:
            self.cart[product_id]['product_count'] = product_count
        else:
            saeed = self.cart[product_id]['product_count'] + product_count
            if saeed > 2:
                print("111111")
                print(self.cart[product_id]['product_count'])
                print(product_count)

                self.cart[product_id]['product_count'] = 2
            else:
                print("222222")
                print(self.cart[product_id]['product_count'])
                print(product_count)
                self.cart[product_id]['product_count'] += product_count
        self.save()

    def remove_product_in_cart(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = models.Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['discount'] = Decimal(item['discount'])
            item['weight'] = Decimal(item['weight'])
            item['total_weight'] = item['weight'] * item['product_count']
            total_price_first = item['price'] * item['discount']
            total_price_second = total_price_first / 100
            one_total = item['price'] - total_price_second
            item['discount_price'] = total_price_second
            item['new_price'] = one_total
            item['total_price'] = one_total * item['product_count']
            item['before_total_price'] = item['price'] * item['product_count']
            yield item

    def get_total_price_before(self):
        return sum(Decimal(item['price']) * item['product_count'] for item in self.cart.values())

    def get_total_price_after(self):
        return sum((Decimal(item['price'])-((Decimal(item['price']) * Decimal(item['discount']))/100)) * item['product_count'] for item in self.cart.values())

    def get_price_discount(self):
        total_one = sum(Decimal(item['price']) * item['product_count'] for item in self.cart.values())
        total_two = sum((Decimal(item['price'])-((Decimal(item['price']) * Decimal(item['discount']))/100)) * item['product_count'] for item in self.cart.values())
        return total_one - total_two

    def get_total_weight_price(self):
        weight =  sum(Decimal(item['weight']) * item['product_count'] for item in self.cart.values())
        if weight < 6000 :
            total_price = 490000
        elif weight > 20000:
                total_price = weight * 70
        else:
            total_price = weight * 90
        return total_price

    def get_total_price_after_and_post(self):
        total = sum((Decimal(item['price'])-((Decimal(item['price']) * Decimal(item['discount']))/100)) * item['product_count'] for item in self.cart.values())
        weight = sum(Decimal(item['weight']) * item['product_count'] for item in self.cart.values())
        if weight < 6000:
            total_price = 490000
        elif weight > 20000:
            total_price = weight * 70
        else:
            total_price = weight * 90
        all_total = total + total_price
        return all_total

