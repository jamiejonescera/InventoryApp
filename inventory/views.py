from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Classroom
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import messages

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
                product_name = request.POST.get('product_name', '').strip()
                quantity = request.POST.get('quantity', '')

                if not product_name or not quantity.isdigit() or int(quantity) <= 0:
                    raise ValueError("Invalid product name or quantity")

                quantity = int(quantity)
                if product_id:  # Editing existing product
                    product = Product.objects.get(id=product_id)
                    product.product_name = product_name
                    product.quantity = quantity
                    product.save()
                else:  # Adding a new product
                    product, created = Product.objects.get_or_create(product_name=product_name)
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

def classroom_view(request):
    classrooms = Classroom.objects.all()
    edit_classroom = None

    # Check for 'edit_id' in GET request to prefill the form for editing
    edit_id = request.GET.get('edit_id')
    if edit_id:
        try:
            edit_classroom = Classroom.objects.get(id=edit_id)
        except Classroom.DoesNotExist:
            messages.error(request, "Classroom not found.")
            return redirect('classroom')  # Redirect if classroom not found

    if request.method == 'POST':
        action = request.POST.get('action')
        classroom_id = request.POST.get('classroom_id', '').strip()
        classroom_name = request.POST.get('classroom_name', '').strip()

        try:
            if action == 'add_or_update':
                if not classroom_name:
                    messages.error(request, "Classroom name cannot be empty.")
                elif classroom_id:  # Editing existing classroom
                    classroom = get_object_or_404(Classroom, id=classroom_id)
                    classroom.classroom_name = classroom_name
                    classroom.save()
                    messages.success(request, "Classroom edited successfully.")
                else:  # Adding a new classroom
                    classroom, created = Classroom.objects.get_or_create(
                        classroom_name=classroom_name,
                        defaults={'capacity': 40}  # Automatically set capacity to 40
                    )
                    if created:
                        messages.success(request, "Classroom added successfully with default capacity.")
                    else:
                        messages.error(request, "Classroom already exists.")

            elif action == 'edit' and classroom_id:
                return redirect(f'{request.path}?edit_id={classroom_id}')

            elif action == 'delete' and classroom_id:
                classroom = get_object_or_404(Classroom, id=classroom_id)
                classroom.delete()
                messages.success(request, "Classroom deleted successfully.")
            else:
                messages.error(request, "Invalid action or missing classroom ID.")

        except Classroom.DoesNotExist:
            messages.error(request, "Classroom not found.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")

        # Redirect after handling form submission to avoid resubmission
        return redirect('classroom')

    return render(request, 'inventory/classroom.html', {
        'classrooms': classrooms,
        'edit_classroom': edit_classroom
    })


class ClassroomListView(APIView):
    def get(self, request):
        try:
            classrooms = Classroom.objects.all().values("id", "classroom_name", "capacity")
            return Response({"classrooms": list(classrooms)}, status=200)
        except Exception as e:
            return Response({"error": f"An error occurred: {e}"}, status=403)
        
class ProductListView(APIView):
    def get(self, request):
        try:
            product = Product.objects.all().values("id", "product_name", "quantity")
            return Response({"products": list(product)}, status=200)
        except Exception as e:
            return Response({"error": f"An error occurred: {e}"}, status=403)