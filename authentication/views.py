from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from django.contrib.auth import  login

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth.models import User



class ProfileView(APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]

    def get(self,request):
        try:
            query = User.objects.get(prouser=request.user.username)
            serializer = ProfileSerializer(query)
            response_message = {"error":False,"data":serializer.data}
        except:
            response_message = {"error":True,"message":"Somthing is Wrong"}
        return Response(response_message)


class UserDataUpdate(APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]

    def post(self,request):
        try:
            user = request.user
            data = request.data
            
            user_obj = User.objects.get(prouser=user)
            print(user_obj)
            user_obj.username = data['username']
            user_obj.email = data['email']
            user_obj.save()

        except:
            response_msg = {"message": "user not updated"}
        return Response(response_msg)


class Updateprofile(APIView):
    permission_classes=[IsAuthenticated, ]
    authentication_classes=[TokenAuthentication, ]

    def post(self,request):
        try:
            user = request.user
            query = User.objects.get(prouser=user)
            data = request.data
            serializers = ProfileSerializer(query,data=data,context={"request":request})
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return_res={"message":"Profile is Updated"}
        except:
            return_res={"message":"Somthing is Wrong Try Agane !"}
        return Response(return_res)


class RegisterView(APIView):
    def post(self,request):
        serializers =UserSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"error":False,"message":f"user is created for '{serializers.data['username']}' ","data":serializers.data})
        return Response({"error":True,"message":"not valid! Try again"})
    

# class LoginView(APIView):
#     # This view should be accessible also for unauthenticated users.
#     permission_classes = (permissions.AllowAny,)

#     # def post(self, request, format=None):
#     #     serializer = LoginSerializer(data=request.data,
#     #         context={ 'request': request })
#     #     serializer.is_valid(raise_exception=True)
#     #     # user = serializer.validated_data['user']
#     #     login(request, user)
#     #     return Response(None, status=status.HTTP_202_ACCEPTED)

#     def post(self, request):
#         user = LoginSerializer(data = request.data)
#         if user.is_valid():
#             return Response(user.data, status = status.HTTP_200_OK)
#         return Response(user.errors, status = status.HTTP_400_BAD_REQUEST)