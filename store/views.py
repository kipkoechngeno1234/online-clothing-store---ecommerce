from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem


# Create your views here.
def home(request):
    return HttpResponseRedirect(reverse('product_list'))

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})


def signup(request):
    """Simple user signup view using Django's built-in UserCreationForm."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile(request):
    """A minimal profile page to demonstrate login protection."""
    return render(request, 'profile.html', {})


@login_required
def add_to_cart(request, pk):
    """Add a product to the user's cart."""
    product = Product.objects.get(pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    
    # Get or create cart for user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create cart item
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    # If item already exists, increase quantity
    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()
    
    return redirect('view_cart')


@login_required
def view_cart(request):
    """Display the user's shopping cart."""
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)


@login_required
def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')


@login_required
def update_cart_item(request, item_id):
    """Update the quantity of a cart item."""
    cart_item = CartItem.objects.get(id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('view_cart')