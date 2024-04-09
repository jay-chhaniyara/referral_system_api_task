from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import *
from .models import UserModel, Referral
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserRegistrationView(APIView):

    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @swagger_auto_schema(
        operation_description="User Regitrations",
        responses={
            200: "Success",
            400: "Bad Request",
            401: "Unauthorized",
        },
        request_body=UserSerializer,

    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        # to check input data is vaild or not
        if serializer.is_valid():
            referral_code = request.data.get('referral_code')
            # it will check referral code is available or not
            if referral_code:

                try:
                    referred_by = UserModel.objects.get(
                        refer_code=referral_code)

                except UserModel.DoesNotExist:
                    return Response("Referral code is invalid", status=status.HTTP_400_BAD_REQUEST)

                user = serializer.save()
                Referral.objects.create(user=user, referred_by=referred_by)
            else:
                user = serializer.save()

                # it will return user id and sucesse message on user register
            return Response({"user_id": user.id, "message": "User created successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    @swagger_auto_schema(
        operation_description="User Login",
        responses={
            200: "Success",
            400: "Bad Request",
            401: "Unauthorized",
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of the user', format='password'),
            },
            required=['email', 'password'],
        )
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user
        user = authenticate(email=email, password=password)

        # if user is authenticate then genrate token for user
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

# It will give user details based on logged user


class UserDetailsView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            user_data = {
                'id': user.id,
                'name': user.name,
                'refer_code': user.refer_code,
                'referral_code': user.referral_code,
                'timestamp': user.timestamp
            }

            return Response({'user': user_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

# It will give all referral user detail of logged user


class UserReferralView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            referrals = Referral.objects.filter(referred_by=user)
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(referrals, request)
            serializer = ReferralSerializer(result_page, many=True)
            referred_users = paginator.get_paginated_response(serializer.data)

            return Response(referred_users.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
