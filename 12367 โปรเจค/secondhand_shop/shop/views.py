from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'shop/product_list.html', {'products': products, 'categories': categories})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    print(f"ข้อมูลตะกร้าสินค้าใน Session: {cart}") # <--- บรรทัดนี้อยู่ในการเยื้องหน้าที่ถูกต้องของ view_cart
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        total_item_price = product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'total_item_price': total_item_price})
        total_price += total_item_price
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        print(f"ข้อมูลตะกร้าสินค้าก่อนลบ ({product_id}): {cart}")
        if product_id in cart:
            del cart[product_id]
            print(f"ข้อมูลตะกร้าสินค้าหลังลบ ({product_id}): {cart}")
            request.session['cart'] = cart
            request.session.modified = True
    # return redirect('view_cart')
    return render(request, 'shop/cart.html', {'cart_items': [], 'total_price': 0})

def contact(request):
    return render(request, 'shop/contact.html')