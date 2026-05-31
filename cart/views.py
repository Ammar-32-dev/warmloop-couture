from django.shortcuts import render, get_object_or_404, redirect
from myapp.models import Product
from .models import Cart, CartItem
from django.contrib import messages

def cart(request):
    # Get or create cart for authenticated users or session-based cart
    if request.user.is_authenticated:
        cart_obj, created = Cart.objects.get_or_create(user=request.user)
    else:
        # For anonymous users, use session key
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        cart_obj, created = Cart.objects.get_or_create(session_key=session_key)

    # Get cart items with product details
    cart_items = cart_obj.items.all().select_related('product')
    total_items = cart_obj.get_total_items()
    total_price = cart_obj.get_total_price()

    context = {
        'cart': cart_obj,
        'cart_items': cart_items,
        'total_items': total_items,
        'total_price': total_price
    }
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get or create cart
    if request.user.is_authenticated:
        cart_obj, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        cart_obj, created = Cart.objects.get_or_create(session_key=session_key)

    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart_obj,
        product=product,
        defaults={'quantity': 0}
    )

    # Increment quantity
    cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f"{product.title} added to cart successfully!")
    return redirect('cart:cart')

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get cart
    if request.user.is_authenticated:
        try:
            cart_obj = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            messages.warning(request, "Cart not found.")
            return redirect('cart:cart')
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        try:
            cart_obj = Cart.objects.get(session_key=session_key)
        except Cart.DoesNotExist:
            messages.warning(request, "Cart not found.")
            return redirect('cart:cart')

    # Remove cart item
    try:
        cart_item = CartItem.objects.get(cart=cart_obj, product=product)
        cart_item.delete()
        messages.success(request, f"{product.title} removed from cart.")
    except CartItem.DoesNotExist:
        messages.warning(request, "Item not found in cart.")

    return redirect('cart:cart')

def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    # Get cart
    if request.user.is_authenticated:
        try:
            cart_obj = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            messages.warning(request, "Cart not found.")
            return redirect('cart:cart')
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        try:
            cart_obj = Cart.objects.get(session_key=session_key)
        except Cart.DoesNotExist:
            messages.warning(request, "Cart not found.")
            return redirect('cart:cart')

    # Update cart item
    if quantity > 0:
        try:
            cart_item = CartItem.objects.get(cart=cart_obj, product=product)
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"{product.title} quantity updated to {quantity}.")
        except CartItem.DoesNotExist:
            messages.warning(request, "Item not found in cart.")
    else:
        # Remove item if quantity is 0
        try:
            cart_item = CartItem.objects.get(cart=cart_obj, product=product)
            cart_item.delete()
            messages.success(request, f"{product.title} removed from cart.")
        except CartItem.DoesNotExist:
            messages.warning(request, "Item not found in cart.")

    return redirect('cart:cart')
