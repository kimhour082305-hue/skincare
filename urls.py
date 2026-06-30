from django.urls import path  # pyrefly: ignore [missing-import]
from . import views

urlpatterns = [
    # Customer Store Front View Paths
    path('', views.index, name='index'),  # 🌟 Kept as 'index' to fix the template crash!
    path('contact/', views.contact_view, name='contact'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Cart Modification and Operations Session Paths
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),

    # Administrative Workspace Dashboard CRUD Actions
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.product_create, name='product_create'),
    path('inventory/edit/<int:product_id>/', views.product_update, name='product_update'),
    path('inventory/delete/<int:product_id>/', views.product_delete, name='product_delete'),
    
    # Wishlist and Checkout Logic
    path('wishlist/add/<int:product_id>/', views.wishlist_add, name='wishlist_add'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/success/', views.order_success_view, name='order_success'),
    
    # Authentication (Login/Signup/Interface) Paths
    path('account/', views.auth_page, name='auth_page'),
    path('account/login/', views.login_view, name='login_view'),   
    path('account/signup/', views.signup_view, name='signup_view'),
    path('account/logout/', views.logout_view, name='logout_view'),
]