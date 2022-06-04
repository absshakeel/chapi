from rest_framework import generics
from Products.serializers import *
from Products.models import *
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from utils.util import Util

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FileUploadParser,FormParser


''' Category
sub category 
'''

class CategoriesViewSet(generics.ListCreateAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializers

class CategoriesUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Categories.objects.all()
    serializer_class =CategoriesSerializers
    lookup_field = 'pk'

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request)
        else:
            return self.list(request)

class SubCategoriesViewSet(generics.ListCreateAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Sub_Categories.objects.all()
    serializer_class = SubCategoriesSerializers

class SubCategoriesUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Sub_Categories.objects.all()
    serializer_class =SubCategoriesSerializers


'''
ProductListview
Product create view
Product update delete view 
'''

class ProductListViewSet(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializers
   

class ProductCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request,format=None):
        data = request.data
        serializer = ProductsSerializers(data=data)
        
        if serializer.is_valid():
            X =  serializer.save()
            product_images = dict((request.data).lists())['product_image']
            for image in product_images:
                modified_data = Util.modify_input_for_multiple_files(image)
                file_serializer = Product_imagesSerializer(data=modified_data)
                if file_serializer.is_valid():
                    file_serializer.save(product=X)
                
                # Product_images.objects.create(image=image,product = X)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetUpDesViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializers
    lookup_field = 'slug'


'''
Supplier List view
Supplier update delete retrieve view
'''

class SupplierView(generics.ListCreateAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class SupplierUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Supplier.objects.all()
    serializer_class =SupplierSerializer



'''
Brnad part
Brand list view
brand update delete view 
'''
class BrandView(generics.ListCreateAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class BrandUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Brand.objects.all()
    serializer_class =BrandSerializer


'''
Country part 
country list create view
country update delete view
'''
class CountryView(generics.ListCreateAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Countreies.objects.all()
    serializer_class = CountriesSerializer

class CountryUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Countreies.objects.all()
    serializer_class =CountriesSerializer


'''
Stock part
Stock list create view
stock update delete view
'''
class StockView(generics.ListCreateAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class StockUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class =StockSerializer


'''Cart and order part
MyCart 
Add to cart 
update cart 
edit cart
delete cart

'''
class MyCart(viewsets.ViewSet):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]
    
    def list(self,request):
        query = Cart.objects.filter(customer=request.user.profile)
        serializers = CartSerializer(query,many=True)
        all_data=[]
        for cart in serializers.data:
            cart_product = CartProduct.objects.filter(cart=cart["id"])
            cart_product_serializer = CartProductSerializer(cart_product,many=True)
            cart["cartproduct"] = cart_product_serializer.data
            all_data.append(cart)
        return Response(all_data)

class AddtoCartView(APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]
    
    def post(self,request):
        product_id = request.data['id']
        product_obj = Products.objects.get(id=product_id)
   
        cart_cart = Cart.objects.filter(customer=request.user.profile).filter(complete=False).first()
        
        try:
            if cart_cart:
                this_product_in_cart = cart_cart.cartproduct_set.filter(product=product_obj)
                if this_product_in_cart.exists():
                    cartprod_uct = CartProduct.objects.filter(product=product_obj).filter(cart__complete=False).first()
                    cartprod_uct.quantity +=1
                    cartprod_uct.subtotal +=product_obj.selling_price
                    cartprod_uct.save()
                    cart_cart.total +=product_obj.selling_price
                    cart_cart.save()

                else:
                    cart_product_new=CartProduct.objects.create(
                        cart = cart_cart,
                        price  =product_obj.selling_price,
                        quantity = 1,
                        subtotal = product_obj.selling_price
                    )
                    cart_product_new.product.add(product_obj)
                    cart_cart.total +=product_obj.selling_price
                    cart_cart.save()

            else:
                Cart.objects.create(customer=request.user.profile,total=0,complete=False)
                new_cart = Cart.objects.filter(customer=request.user.profile).filter(complete=False).first()
                cart_product_new=CartProduct.objects.create(
                        cart = new_cart,
                        price  =product_obj.selling_price,
                        quantity = 1,
                        subtotal = product_obj.selling_price
                    )
                cart_product_new.product.add(product_obj)
                # print("NEW CART PRODUCT CREATED")    
                new_cart.total +=product_obj.selling_price
                new_cart.save()

            response_mesage = {'error':False,'message':"Product add to card successfully","productid":product_id}
        except:
            response_mesage = {'error':True,'message':"Product Not add!Somthing is Wromg"}

        return Response(response_mesage)



class Updatecart(APIView):

    def post(self,request):
        cart_product_id = request.data['id']
        cart_product = CartProduct.objects.get(id=cart_product_id)
        
        cart_obj = CartProduct.cart

        cart_product.quantity += 1
        cart_obj.subtotal +=cart_product.price
        cart_product.save()

        cart_obj.total += cart_product.price
        cart_obj.save() 

        return Response({'message': "CartProduct is added"})

class Editcart(APIView):

    def post(self,request):
        cart_product_id = request.data['id']
        cart_product = CartProduct.objects.get(id=cart_product_id)
        cart_obj = CartProduct.cart

        cart_product.quantity -= 1
        cart_obj.subtotal -=cart_product.price
        cart_product.save()

        cart_obj.total -= cart_product.price
        cart_obj.save() 
        
        if cart_product.quantity == 0:
            cart_product.delete()

        return Response({'message': "CartProduct is added"})

class DeleteCart(APIView):
    def post(self,request):
        cart_product = CartProduct.objects.get(id = request.data['id'])
        cart_product.delete()


'''
Order list
Order create
retrieve 
delete view
'''
class OrderViewset(viewsets.ViewSet):
    authentication_classes=[TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def list(self,request):
        query = Order.objects.filter(cart__customer = request.user.profile)
        serializers = OrderSerializer(query,many=True)
        all_data = []
        for order in serializers.data:
            cartproduct = CartProduct.objects.filter(cart_id=order['cart']['id'])
            cartproduct_serializer = CartProductSerializer(cartproduct,many=True)
            order['cartproduct'] = cartproduct_serializer.data
            all_data.append(order)
        return Response(all_data)
    def retrieve(self,request,pk=None):
        try:
            queryset = Order.objects.get(id=pk)
            serializers = OrderSerializer(queryset)
            data = serializers.data
            all_date=[]
            cartproduct = CartProduct.objects.filter(cart_id=data['cart']['id'])
            cartproduct_serializer = CartProductSerializer(cartproduct,many=True)
            data['cartproduct'] = cartproduct_serializer.data
            all_date.append(data)
            response_message = {"error":False,"data":all_date}
        except:
            response_message = {"error":True,"data":"No data Found for This id"}

        return Response(response_message)

    def destroy(self,request,pk=None):
        try:
            order_obj=Order.objects.get(id=pk)
            cart_obj = Cart.objects.get(id=order_obj.cart.id)
            order_obj.delete()
            cart_obj.delete()
            responsemessage = {"erroe":False,"message":"Order delated","order id":pk}
        except:
            responsemessage = {"erroe":True,"message":"Order Not Found"}
        return Response(responsemessage)

    def create(self,request):
        cart_id = request.data["cartId"]
        cart_obj = Cart.objects.get(id=cart_id)
        address = request.data["address"]
        mobile = request.data["mobile"]
        email = request.data["email"]
        cart_obj.complit=True
        cart_obj.save()
        created_order = Order.objects.create(
            cart=cart_obj,
            address=address,
            mobile=mobile,
            email=email,
            total=cart_obj.total,
            discount=3,
        )
        return Response({"message":"order Resebed","cart id":cart_id,"order id":created_order.id})
