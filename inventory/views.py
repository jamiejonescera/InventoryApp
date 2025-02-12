from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Classroom, Request
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from datetime import timedelta
from django.http import JsonResponse
# views.py
from django.views import View
from django.shortcuts import render
from .models import Request
from django.views.decorators.csrf import csrf_protect

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
        capacity = request.POST.get('capacity', '').strip()
        facility_type = request.POST.get('facility_type', '').strip()
        classroom_status = request.POST.get('classroom_status', '').strip()

        try:
            if action == 'add_or_update':
                if not classroom_name or not capacity.isdigit() or int(capacity) <= 0:
                    messages.error(request, "Invalid classroom name or capacity or facility type.")
                elif classroom_id:  # Editing existing classroom
                    classroom = get_object_or_404(Classroom, id=classroom_id)
                    classroom.classroom_name = classroom_name
                    classroom.capacity = int(capacity)
                    classroom.facility_type = facility_type
                    classroom.classroom_status = classroom_status
                    classroom.save()
                    messages.success(request, "Classroom edited successfully.")
                else:  # Adding a new classroom
                    classroom, created = Classroom.objects.get_or_create(
                        classroom_name=classroom_name,
                        facility_type = facility_type,
                        classroom_status = classroom_status,
                        defaults={'capacity': int(capacity)}
                        
                    )
                    if created:
                        messages.success(request, "Classroom added successfully.")
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
            classrooms = Classroom.objects.all().values("id", "classroom_name", "capacity", "facility_type", "classroom_status")
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
        

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Classroom
from .serializers import ClassroomSerializer

class ClassroomListView(APIView):
    def get(self, request):
        classrooms = Classroom.objects.all()
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for rendering the requests management page



def request_list(request):
    requests = Request.objects.all().values(
        "id", "staff_name", "product_name", "quantity_requested", "purpose", "request_status"
    )
    return JsonResponse(list(requests), safe=False)

class RequestManagementView(View):
    def get(self, request):
        requests = Request.objects.all().order_by('-created_at').values()
        return JsonResponse(list(requests), safe=False)
@csrf_exempt  # This disables CSRF protection for this view
def handle_request_action(request):
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        action = request.POST.get("action")

        req = get_object_or_404(Request, id=request_id)
        if action == "approve":
            req.request_status = "Approved"
        elif action == "deny":
            req.request_status = "Denied"
        req.save()

        return JsonResponse({"message": f"Request {action}d successfully"})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

# Notification endpoint for new requests (example: AJAX polling or WebSocket integration)
def get_notifications(request):
    if request.method == "GET":
        # Fetch new requests (Example: requests created in the last 5 minutes)
        recent_requests = Request.objects.filter(created_at__gte=now() - timedelta(minutes=5))
        data = {
            "count": recent_requests.count(),
            "requests": list(recent_requests.values("id", "requester_name", "description", "created_at"))
        }
        return JsonResponse(data)
    
    class ClassroomListView(View):
        def get(self, request):
            classrooms = Classroom.objects.values('name', 'capacity')  # Fetch only name & capacity
            return JsonResponse(list(classrooms), safe=False)  # Convert QuerySet to list