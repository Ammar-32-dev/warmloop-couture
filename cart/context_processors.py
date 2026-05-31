from .models import Cart

def cart_globals(request):
    cart_obj = None
    total_items = 0
    
    if request.user.is_authenticated:
        cart_obj, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if session_key:
            cart_obj, created = Cart.objects.get_or_create(session_key=session_key)
            
    if cart_obj:
        total_items = cart_obj.get_total_items()
        
    return {
        'global_cart': cart_obj,
        'global_total_items': total_items,
    }
