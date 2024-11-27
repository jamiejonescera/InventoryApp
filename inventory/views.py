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

def classroom_view(request):
    classrooms = Classroom.objects.all()
    edit_classroom = None  # To store the classroom being edited

    if request.method == 'POST':
        action = request.POST.get('action')
        classroom_id = request.POST.get('classroom_id')
        
        try:
            if action == 'add_or_update':
                # Add or Update logic
                classroom_name = request.POST.get('classroom_name', '').strip()

                if not classroom_name:
                    messages.error(request, "Classroom name cannot be empty")
                    return render(request, 'inventory/classroom.html', {'classrooms': classrooms})

                if classroom_id:  # Editing existing classroom
                    classroom = Classroom.objects.get(id=classroom_id)
                    classroom.classroom_name = classroom_name
                    classroom.save()
                    messages.success(request, "Edited Successfully!")
                    return render(request, 'inventory/classroom.html', {"classrooms": classroom})
                    
                    
                else:  # Adding a new classroom
                    classroom, created = Classroom.objects.get_or_create(classroom_name=classroom_name)
                    if not created:
                        messages.error(request, "Classroom already exists")

            elif action == 'edit' and classroom_id:
                edit_classroom = get_object_or_404(Classroom, id=classroom_id)

            elif action == 'delete' and classroom_id:
                Classroom.objects.filter(id=classroom_id).delete()

            messages.success(request, "Success!")
            return render(request, 'inventory/classroom.html', {
                'classrooms': classrooms,
                'edit_classroom': edit_classroom
            })
        
        except Exception as e:
            messages.error(request, "Failed to Add a Classroom...")
    else:
         messages.error(request, "Request is not a POST method.")
         return render(request, 'inventory/classroom.html', {'classrooms': classrooms})

class ClassroomListView(APIView):
    def get(self, request):
        try:
            classrooms = Classroom.objects.all().values(
                "id",
                "classroom_name"
            )
            
            return Response({"classrooms": list(classrooms)}, status=200)
        except Exception as e:
            return Response({"error": "An error has occured"}, status=403)