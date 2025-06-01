from django.urls import path
from .apps import PaymentFormsConfig
from .views import create_payment_intent, item_detail, create_payment_intent_order, order_detail, add_item_to_order, remove_item_from_order


app_name = PaymentFormsConfig.name


urlpatterns = [
    path('item/<int:pk>/', item_detail, name='item_detail'),
    path('buy/<int:pk>/', create_payment_intent, name='create_payment_intent'),

    path('order/<int:pk>/', order_detail, name='order_detail'),
    path('buy/order/<int:pk>/', create_payment_intent_order, name='create_payment_intent_order'),
    path('order/<int:order_id>/add-item/<int:item_id>/', add_item_to_order, name='add_item_to_order'),
    path('order/<int:order_id>/remove-item/<int:item_id>/', remove_item_from_order, name='remove_item_from_order'),
]

