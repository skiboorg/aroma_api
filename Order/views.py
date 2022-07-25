from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import *
from Cart.models import *
from user.models import *
from .serializers import *
import requests
import settings

import json
from django.core.mail import send_mail
from django.template.loader import render_to_string


def init_payment(order):
    headers = {
                  'Content-Type': 'application/json',
                }
    order_items = order.order_items.all()
    order_user = order.user
    items = []

    for order_item in order_items:
        items.append(
            {
                "Name": order_item.item.name,
                "Price": order_item.item.price * 100,
                "Quantity": order_item.amount,
                "Amount": order_item.price * 100,
                "PaymentMethod": "full_payment",
                "PaymentObject": "commodity",
                "Tax": "vat10",
                "Ean13": ""
            },
        )

    payload = {
        "TerminalKey": settings.TERMINAL_ID,
        "Amount": order.price * 100,
        "OrderId": order.id,
        "Description": f'Оплата заказа №{order.id}',
        "NotificationURL": 'https://artdox.ru/api/order/payment_notify',
        # "DATA": {
        #     "Phone": "+71234567890",
        #     "Email": "a@test.com"
        # },
        "Receipt": {
            "Email": order.user.email,
            "Phone": order.user.phone,
            "Taxation": "osn",
            "Items": items
        }
    }
    #print(payload)
    response = requests.post(settings.INIT_PAYMENT_URL, data=json.dumps(payload), headers=headers)
    response_json = response.json()
    print(response_json)
    if response_json['Success']:
        #print(response_json['PaymentURL'])
        return {'success': True, 'payment_url':response_json['PaymentURL'],'order_id':order.id}
    else:
        return {'success': False}

class CreateOrder(APIView):
    def post(self,request):
        print(self.request.data.get('session_id'))
        if self.request.user.is_authenticated:
            cart = Cart.objects.get(user=self.request.user)
        else:
            cart = Cart.objects.get(session_id=self.request.data.get('session_id'))


        if self.request.user.is_authenticated:
            new_order = Order.objects.create(user=request.user,
                                             delivery=request.data.get('delivery'),
                                             address=request.data.get('address'),
                                             )
        else:
            new_order = Order.objects.create(session_id=self.request.data.get('session_id'),
                                             delivery=request.data.get('delivery'),
                                             address=request.data.get('address'),
                                             )



        for item in cart.items.all():
            OrderItem.objects.create(order=new_order,
                                     item=item.item,
                                     amount=item.amount)

            item.item.left -= item.amount
            item.item.save()
            request.user.total_amount += item.amount
            item.delete()

        cart.price = 0
        cart.save()

        request.user.total_summ += new_order.price
        request.user.save()

        # Transaction.objects.create(user=self.request.user,
        #                            amount=new_order.price,
        #                            is_buy=True,
        #                            type='CARD')
        result = init_payment(new_order)
        # result = ''
        # msg_html = render_to_string('order.html', {'order': new_order})
        #
        # send_mail('Ваш заказ', None, settings.SMTP_FROM, [settings.ADMIN_EMAIL],
        #           fail_silently=False, html_message=msg_html)
        return Response(result, status=200)


class GetOrders(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


def get_client_token():
    response = requests.post('https://api.saferoute.ru/v2/auth/login',
                             {'email': settings.SAFEROUTE_LOGIN,
                              'password': settings.SAFEROUTE_PASS
                              })
    return response.json()['token']

class GetDeliveryData(APIView):
    def get(self, request):

        print(get_client_token())
        headers = {
            'Authorization' : f'Bearer {get_client_token()}'
        }
        # response = requests.get('https://api.saferoute.ru/v2/lists/delivery-companies',headers=headers)
        response = requests.get('https://api.saferoute.ru/v2/lists/points?companyId=178',headers=headers)
        print(response.json())

        return Response(response.json(), status=200)
