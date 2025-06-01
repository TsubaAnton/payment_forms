from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import Item, Order
from django.conf import settings
import stripe
from django.http import JsonResponse


@csrf_exempt
def create_payment_intent(request, pk):
    item = get_object_or_404(Item, pk=pk)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(item.price * 100),
            currency=item.currency,
            description=f"Оплата {item.name}",
            automatic_payment_methods={"enabled": True},
        )
        return JsonResponse({
            'clientSecret': payment_intent.client_secret,
            'publicKey': settings.STRIPE_PUBLIC_KEY
        })
    except stripe.error.StripeError as e:
        return JsonResponse({'Ошибка': str(e)})


@csrf_exempt
def create_payment_intent_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    currency = order.items.first().currency if order.items.exists() else 'usd'
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=order.calculate_total(),
            currency=currency,
            description=f"Оплата Заказа {order.id}",
            automatic_payment_methods={'enabled': True},
        )
        return JsonResponse({
            'clientSecret': payment_intent.client_secret,
            'publicKey': settings.STRIPE_PUBLIC_KEY
        })
    except stripe.error.StripeError as e:
        return JsonResponse({'Ошибка': str(e)})


def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'payment_forms/item_detail.html',
                  {'item': item, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    all_items = Item.objects.all()
    return render(request, 'payment_forms/order_detail.html',
                  {'order': order, 'all_items': all_items,  'stripe_public_key': settings.STRIPE_PUBLIC_KEY})


@csrf_exempt
def add_item_to_order(request, order_id, item_id):
    order = get_object_or_404(Order, pk=order_id)
    item = get_object_or_404(Item, pk=item_id)

    if not order.items.filter(pk=item.id).exists():
        order.items.add(item)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Предмет уже в заказе'})


@csrf_exempt
def remove_item_from_order(request, order_id, item_id):
    order = get_object_or_404(Order, pk=order_id)
    item = get_object_or_404(Item, pk=item_id)

    if order.items.filter(pk=item.id).exists():
        order.items.remove(item)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Предмет не в заказе'})
