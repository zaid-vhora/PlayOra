from .cart import Cart
from wishlist.wishlist import Wishlist

def cart_total_amount(request):
    cart = Cart(request)
    wishlist = Wishlist(request)
    total_bill = 0
    count = 0
    for key, value in cart.cart.items():
        total_bill += float(value['price']) * int(value['quantity'])
        count += int(value['quantity'])
    return {
        'cart_total_amount': total_bill,
        'cart_count': count,
        'wishlist_count': len(wishlist.wishlist)
    }
