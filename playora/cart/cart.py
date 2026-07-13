from decimal import Decimal
from django.conf import settings
from app_modules.adminapp.models import toy

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, action=None):
        id = str(product.id)
        if id not in self.cart:
            self.cart[id] = {
                'userid': product.added_by.id if product.added_by else None,
                'product_id': id,
                'name': product.name,
                'quantity': 1,
                'price': str(product.rental_price_per_week),
                'security_deposit': str(product.security_deposit),
                'image': product.image.url if product.image else ''
            }
        else:
            for key, value in self.cart.items():
                if key == id:
                    value['quantity'] = value['quantity'] + 1
                    break
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrement(self, product):
        for key, value in self.cart.items():
            if key == str(product.id):
                value['quantity'] = value['quantity'] - 1
                if value['quantity'] < 1:
                    self.remove(product)
                self.save()
                break

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
