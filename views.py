from django.shortcuts import render, redirect, get_object_or_404  # pyrefly: ignore [missing-import]
from django.core.paginator import Paginator
from .models import Product, Category
from .forms import ProductForm
from django.contrib.auth import login, authenticate, logout  # pyrefly: ignore [missing-import]
from django.contrib.auth.models import User  # pyrefly: ignore [missing-import]
from django.contrib import messages  # pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required  # pyrefly: ignore [missing-import]
from django.contrib.admin.views.decorators import staff_member_required

# =====================================================================
# 🔑 AUTHENTICATION & USER MANAGEMENT VIEWS
# =====================================================================

def auth_page(request):
    # If a user is already signed in, don't show them the login screen; send them to the store
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'store/login.html')

def signup_view(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        e_mail = request.POST.get('email')
        p_word = request.POST.get('password')
        
        if User.objects.filter(username=u_name).exists():
            messages.error(request, "Username is already taken.")
            return redirect('auth_page')
            
        user = User.objects.create_user(username=u_name, email=e_mail, password=p_word)
        user.save()
        
        login(request, user)
        return redirect('index')  
    return redirect('auth_page')

def login_view(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        
        user = authenticate(request, username=u_name, password=p_word)
        if user is not None:
            login(request, user)
            return redirect('index')  
        else:
            messages.error(request, "Invalid authentication credentials.")
    return redirect('auth_page')

# 🌟 NEW: Handles logging out and safely returning back to the homepage storefront
def logout_view(request):
    logout(request)
    return redirect('index')


# =====================================================================
# 🛒 PART A: CLIENT STOREFRONT VIEWS
# =====================================================================

# 1. Main Store Homepage Catalog Display
def index(request):
    products = Product.objects.all()
    
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
        
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)

    brand_query = request.GET.get('brand')
    if brand_query:
        products = products.filter(brand__iexact=brand_query)

    promotion = request.GET.get('promotion')
    if promotion == 'true':
        products = products.filter(discount_percentage__gt=0)

    # Apply pagination: 8 products per page
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    context = {
        'products': page_obj,
        'categories': categories,
    }
    return render(request, 'store/index.html', context)

def contact_view(request):
    if request.method == 'POST':
        messages.success(request, "Your message has been successfully sent! We will get back to you shortly.")
        return redirect('contact')
    return render(request, 'store/contact.html')

# 2. Premium Product Details Screen Layout
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


# =====================================================================
# 🛍️ PART B: SHOPPING CART SESSION LOGIC
# =====================================================================

# 3. Add Line Items to Browser Storage Session
# 🌟 UPDATED: Restricts guests from adding items until they sign in
@login_required(login_url='auth_page')
def cart_add(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # Grab current session cart or start a fresh dict
        cart = request.session.get('cart', {})
        pid_str = str(product_id)
        
        if pid_str in cart:
            cart[pid_str]['quantity'] += quantity
        else:
            cart[pid_str] = {
                'name': product.name,
                'price': float(product.price),
                'image_url': product.image.url,
                'quantity': quantity
            }
        
        request.session['cart'] = cart
    return redirect('cart_detail')

# 4. View Bag Contents & Calculations
def cart_detail(request):
    cart = request.session.get('cart', {})
    total_bill = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'store/cart.html', {'cart': cart, 'total_bill': total_bill})

# 5. Remove Item completely from Session Dictionary
def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    pid_str = str(product_id)
    if pid_str in cart:
        del cart[pid_str]
        request.session['cart'] = cart
    return redirect('cart_detail')


# =====================================================================
# ⚙️ PART C: ADMINISTRATIVE INVENTORY CRUD LOGIC
# =====================================================================

# 6. READ: Inventory Workspace Grid Listing
@staff_member_required(login_url='auth_page')
def inventory_list(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'store/product_list.html', {'products': products})

# 7. CREATE: Save Fresh Product Rows to Database
@staff_member_required(login_url='auth_page')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = ProductForm()
    return render(request, 'store/product_form.html', {'form': form, 'title': 'Add New Product'})

# 8. UPDATE: Edit Pre-existing Item Properties
@staff_member_required(login_url='auth_page')
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_form.html', {'form': form, 'title': 'Update Product'})

# 9. DELETE: Safely Purge Records from Database
@staff_member_required(login_url='auth_page')
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('inventory_list')
    return render(request, 'store/product_confirm_delete.html', {'product': product})


# =====================================================================
# ⚙️ PART D: EXTRA APP LOGIC
# =====================================================================

# 10. INTERACTIVE WISH LIST LOGIC
def wishlist_add(request, product_id):
    if request.method == 'POST':
        wishlist = request.session.get('wishlist', [])
        
        # Toggle mechanism: If it's already there, remove it. Otherwise, add it!
        if product_id in wishlist:
            wishlist.remove(product_id)
        else:
            wishlist.append(product_id)
            
        request.session['wishlist'] = wishlist
    
    # Redirect back safely to the page the user was looking at
    return redirect('product_detail', product_id=product_id)

# 11. Checkout Security Gate
# 🌟 UPDATED: Forces a redirect to your beautiful auth page if they aren't logged in
@login_required(login_url='auth_page')
def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')
        
    total_bill = sum(item['price'] * item['quantity'] for item in cart.values())
    
    if request.method == 'POST':
        # Clear the shopping cart session data upon payment completion
        request.session['cart'] = {}
        return redirect('order_success') 
        
    return render(request, 'store/checkout.html', {'cart': cart, 'total_bill': total_bill})

# 12. Finalized Checkout Land Screen
def order_success_view(request):
    return render(request, 'store/order_success.html')
