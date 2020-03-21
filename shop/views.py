from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Products, Order, OrderProduct
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm


# Create your views here.
def index(request):
    items = Products.objects.all()
    context = {
        'items': items
    }
    return render(request, 'main/home.html', context)


def detail(request):
    return render(request, 'main/product_de.html')


class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'main/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        print(self.request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            print("This form is valid")
            return redirect('main:checkout')
        return redirect('main:checkout')


class HomeView(ListView):
    model = Products
    paginate_by = 9
    template_name = "main/home.html"


class DetailProductView(DetailView):
    model = Products
    template_name = "main/product_de.html"


class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "main/order-summary.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have any active order")
            return redirect('/')


@login_required()
def add_to_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)
    order_item, created = OrderProduct.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs:
        order = order_qs[0]
        if order.item.filter(item__slug=item.slug):
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Successfully updated your cart")
            return redirect('main:order-summary')
        else:
            order.item.add(order_item)
            messages.info(request, "Successfully added this item in your cart")
            return redirect('main:order-summary')
    else:
        order_date = timezone.now()
        orders = Order.objects.create(user=request.user, ordered_date=order_date)
        orders.item.add(order_item)
        messages.info(request, "Successfully added this item in your cart")
    return redirect('main:order-summary')


@login_required()
def remove_from_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs:
        order = order_qs[0]
        if order.item.filter(item__slug=item.slug):
            order_item = OrderProduct.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.item.remove(order_item)
            messages.warning(request, "This item was removed from your cart")
            return redirect('main:product-detail', slug=slug)
        else:
            messages.info(request, "You don't have this item in your cart")
            return redirect('main:product-detail', slug=slug)

    else:
        messages.info(request, "Your cart is empty")
        return redirect('main:product-detail', slug=slug)


@login_required()
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs:
        order = order_qs[0]
        if order.item.filter(item__slug=item.slug):
            order_item = OrderProduct.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.item.remove(order_item)
            messages.warning(request, "Removed one unit for this item")
            return redirect('main:order-summary')
        else:
            messages.info(request, "You don't have this item in your cart")
            return redirect('main:product-detail', slug=slug)

    else:
        messages.info(request, "Your cart is empty")
        return redirect('main:product-detail', slug=slug)
