from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()

            # إرسال تحديث عبر WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "products",
                {
                    "type": "send_update",
                    "message": f"تمت إضافة منتج جديد: {product.name}"
                }
            )

            print(f"📢 WebSocket Sent: {product.name}")  # ✅ تحقق من الإرسال
            # return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})


def get_products_json(request):
    products = list(Product.objects.values())
    return JsonResponse({'products': products})