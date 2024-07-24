from cart.cart import Cart, Shipping


def cart(request):
    return {'cart': Cart(request)}


def location_cart(request):
    return {'location': Shipping(request)}

