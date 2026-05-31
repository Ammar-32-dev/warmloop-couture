from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Category

def product_list(request):
    category_slug = request.GET.get('category')
    selected_category = None
    products = Product.objects.filter(available=True)
    
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
        
    return render(request, 'myapp/product_list.html', {
        'products': products,
        'selected_category': selected_category
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    return render(request, 'myapp/product_detail.html', {'product': product})

def signup_view(request):
    """
    Handles premium custom registration. Autologs in the user on success.
    """
    if request.user.is_authenticated:
        return redirect('myapp:product_list')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('myapp:product_list')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})

def login_view(request):
    """
    Handles standard customer authentication log-ins.
    """
    if request.user.is_authenticated:
        return redirect('myapp:product_list')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('myapp:product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

def logout_view(request):
    """
    Terminates active session and redirects back to the main storefront.
    """
    logout(request)
    return redirect('myapp:product_list')
