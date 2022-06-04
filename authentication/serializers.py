from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token



User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",'username','password','first_name','last_name','email')
        extra_kwargs = { 'password':{'write_only': True, 'required': True}}

    def create(self,validated_data):
            user = User.objects.create_user(**validated_data)
            Token.objects.create(user=user)
            Profile.objects.create(prouser=user)
            return user 

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ['prouser']
    
    def validate(self,attrs):
        attrs['prouser'] = self.context['request'].user

    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['prouser'] = UserSerializer(instance.prouser).data
        return response


# class LoginSerializer(serializers.Serializer):
#     """
#     This serializer defines two fields for authentication:
#       * username
#       * password.
#     It will try to authenticate the user with when validated.
#     """
#     username = serializers.CharField(
#         label="Username",
#         write_only=True
#     )
#     password = serializers.CharField(
#         label="Password",
#         # This will be used when the DRF browsable API is enabled
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#         write_only=True
#     )
    # def validate(self, data):
    #     # email = data["email"]
    #     username = data['username']
    #     password = data["password"]
    #     user = User.objects.get(username = username,password=password)
    #     if user:
    #         return data
    #     raise serializers.ValidationError("User Not Found")

    # def validate(self, attrs):
    #     # Take username and password from request
    #     username = attrs.get('username')
    #     password = attrs.get('password')

    #     if username and password:
    #         # Try to authenticate the user using Django auth framework.
    #         user = authenticate(request=self.context.get('request'),
    #                             username=username, password=password)
    #         if not user:
    #             # If we don't have a regular user, raise a ValidationError
    #             msg = 'Access denied: wrong username or password.'
    #             raise serializers.ValidationError(msg, code='authorization')
    #     else:
    #         msg = 'Both "username" and "password" are required.'
    #         raise serializers.ValidationError(msg, code='authorization')
    #     # We have a valid user, put it in the serializer's validated_data.
    #     # It will be used in the view.
    #     attrs['user'] = user
    #     return attrs