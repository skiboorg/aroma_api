from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *


def calcCart(cart):
    items = cart.items.all()
    price = 0
    for item in items:
        price+=item.price
    cart.price = price
    cart.save()

class GetCart(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    def get_object(self):
        print('ss')
        if self.request.user.is_authenticated:
            return Cart.objects.get(user=self.request.user)
        else:
            cart, created = Cart.objects.get_or_create(session_id=self.request.query_params.get('session_id'))
            if created:
                print('new cart created')
            return cart


class ChangeAmount(APIView):
    def post(self, request):
        id= request.data['id']
        action= request.data['action']
        item = CartItem.objects.get(id=id)
        cart = item.cart
        if action == 'del':
            if item.amount == 1:
                item.delete()
            else:
                item.amount -= 1
                item.save()
            calcCart(cart)
        if action == 'add':
            item.amount +=1
            item.save()
            calcCart(cart)
        return Response(status=200)

class DeleteItem(APIView):
    def post(self,request):
        data = request.data

        CartItem.objects.get(id=data['id']).delete()
        if self.request.user.is_authenticated:
            cart = Cart.objects.get(user=self.request.user)
        else:
            cart = Cart.objects.get(session_id=self.request.data.get('session_id'))
        calcCart(cart)
        return Response(status=200)


class AddToCart(APIView):
    def post(self,request):
        if self.request.user.is_authenticated:
            cart = Cart.objects.get(user=self.request.user)
        else:
            cart = Cart.objects.get(session_id=self.request.data.get('session_id'))

        data = request.data
        try:
            item = CartItem.objects.get(item_id=data['id'],
                                        cart=cart,
                                        volume_id=data['cartData']['selectedVolume']['id'],
                                        box=data['cartData']['selectedBox']
                                        )
            item.amount += data['amount']
            item.save()
        except:
            item = CartItem.objects.create(
                item_id=data['id'],
                cart=cart,
                volume_id=data['cartData']['selectedVolume']['id'],
                box=data['cartData']['selectedBox'],
                amount = data['amount'])
        return Response(status=200)