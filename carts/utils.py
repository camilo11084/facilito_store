from .models import Cart


def get_or_create_cart(request):
    user = request.user if request.user.is_authenticated else None
    card_id = request.session.get('cart_id')#none
    cart = Cart.objects.filter(cart_id=card_id).first()  #[]->none

    if cart is None:
        cart = Cart.objects.create(user=user)


    if user and cart.user is None:
        cart.user = user
        cart.save()


    request.session['cart_id'] = cart.cart_id

    return cart

def destroy_cart(request):
    request.session['cart_id'] = None