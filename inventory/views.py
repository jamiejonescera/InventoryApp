from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def inventory_view(request):
    products = Product.objects.all()
    error = None
    edit_product = None  # To store the product being edited

    if request.method == 'POST':
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')
        
        try:
            if action == 'add_or_update':
                # Add or Update logic
                name = request.POST.get('name', '').strip()
                quantity = request.POST.get('quantity', '')

                if not name or not quantity.isdigit() or int(quantity) <= 0:
                    raise ValueError("Invalid product name or quantity")

                quantity = int(quantity)
                if product_id:  # Editing existing product
                    product = Product.objects.get(id=product_id)
                    product.name = name
                    product.quantity = quantity
                    product.save()
                else:  # Adding a new product
                    product, created = Product.objects.get_or_create(name=name)
                    if not created:  # If product exists, increase the quantity
                        product.quantity += quantity
                    else:
                        product.quantity = quantity
                    product.save()

            elif action == 'edit' and product_id:
                # Fetch the product to be edited
                edit_product = get_object_or_404(Product, id=product_id)

            elif action == 'delete' and product_id:
                # Delete logic
                Product.objects.filter(id=product_id).delete()

        except Exception as e:
            error = str(e)

        # Refresh page after edit or delete
        return render(request, 'inventory/inventory.html', {
            'products': products,
            'error': error,
            'edit_product': edit_product
        })

    return render(request, 'inventory/inventory.html', {'products': products, 'error': error})
