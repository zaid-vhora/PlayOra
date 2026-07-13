class Wishlist(object):
    def __init__(self, request):
        self.session = request.session
        wishlist = self.session.get('wishlist')
        if not wishlist:
            wishlist = self.session['wishlist'] = {}
        self.wishlist = wishlist

    def add(self, product):
        id = str(product.id)
        if id not in self.wishlist:
            self.wishlist[id] = {
                'product_id': id,
                'name': product.name,
                'price': str(product.rental_price_per_week),
                'image': product.image.url if product.image else ''
            }
            self.save()

    def save(self):
        self.session['wishlist'] = self.wishlist
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.wishlist:
            del self.wishlist[product_id]
            self.save()

    def clear(self):
        self.session['wishlist'] = {}
        self.session.modified = True
