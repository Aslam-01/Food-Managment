from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from .models import FoodProduct
from .serializers import FoodProductSerializer, UserLoginSerializer, UserSignupSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
import random
from drf_yasg import openapi

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserSignupView(APIView):
    @swagger_auto_schema(request_body=UserSignupSerializer)
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_token_for_user(user)
            return Response({'msg': 'Register Successful', 'token': token}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_token_for_user(user)
                return Response({"token": token, "msg": "Login Successful"}, status=status.HTTP_200_OK)
            return Response({"errors": {"validation_errors": ['password and email is not valid']}}, status=status.HTTP_404_NOT_FOUND)

class ProductView(APIView):
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(name='min_price', in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        openapi.Parameter(name='max_price', in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        openapi.Parameter(name='average_rating', in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        openapi.Parameter(name='category', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(name='toppings', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(name='type', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        filters = {}
        filter_mapping = {
            'min_price': 'price__gte',
            'max_price': 'price__lte',
            'average_rating': 'average_rating__gte',
            'category': 'category__in',
            'toppings': 'customization__toppings__in',
            'type': 'product_type',
        }

        for param, field in filter_mapping.items():
            values = self.request.query_params.getlist(param) if param == 'category' else self.request.query_params.get(param)
            if values:
                values = values.capitalize() if isinstance(values, str) else [value.capitalize() for value in values]
                filters[field] = values

        try:
            foods = FoodProduct.objects.filter(**filters)
            serializer = FoodProductSerializer(foods, many=True)
            page = self.pagination_class().paginate_queryset(serializer.data, self.request)
            if page is not None:
                return self.get_paginated_response(page)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=FoodProductSerializer,manual_parameters=[
        openapi.Parameter(name = 'Authorization', in_=openapi.IN_HEADER, description="Please Provide Bearer JWT token", type=openapi.TYPE_STRING)
    ])
    def post(self, request):
        if not request.user.is_admin:
            raise PermissionDenied("You do not have permission to perform this action.")
        
        try:
            serializer = FoodProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': f"{serializer.data['name']} Is Added Successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request, pk):
        try:
            food = FoodProduct.objects.get(pk=pk)
            serializer = FoodProductSerializer(food)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=FoodProductSerializer,manual_parameters=[
        openapi.Parameter(name = 'Authorization', in_=openapi.IN_HEADER, description="Please Provide Bearer JWT token", type=openapi.TYPE_STRING)
    ])
    def put(self, request, pk):
        data = request.data 
        try:
            existing_food = FoodProduct.objects.get(pk=pk)
            serializer = FoodProductSerializer(existing_food, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'msg': f'{existing_food.name} is updated'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(request_body=FoodProductSerializer,manual_parameters=[
        openapi.Parameter(name = 'Authorization', in_=openapi.IN_HEADER, description="Please Provide Bearer JWT token", type=openapi.TYPE_STRING)
    ])
    def patch(self, request, pk):
        data = request.data 
        try:
            existing_food = FoodProduct.objects.get(pk=pk)
            serializer = FoodProductSerializer(existing_food, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'msg': f'{existing_food.name} is updated'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(name = 'Authorization', in_=openapi.IN_HEADER, description="Please Provide Bearer JWT token", type=openapi.TYPE_STRING)
    ])
    def delete(self, request, pk):
        if not request.user.is_admin:
            raise PermissionDenied("You do not have permission to perform this action.")

        try:
            food = FoodProduct.objects.get(pk=pk)
            food.delete()
            return Response({'msg': f'{food.name} deleted'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AddFvrtFood(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(name = 'Authorization', in_=openapi.IN_HEADER, description="Please Provide Bearer JWT token", type=openapi.TYPE_STRING)
    ])
    def post(self, request, food_id):
        user = request.user
        try:
            food = FoodProduct.objects.get(pk=food_id)
            if food.fvrt_by.filter(pk=user.id).exists():
                return Response({'msg': f"{food.name} is already in favourite list"}, status=status.HTTP_400_BAD_REQUEST)
            food.fvrt_by.add(user)
            return Response({'msg': f"{food.name} added to favourite"})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetFvrtFood(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(name = 'Authorization', in_=openapi.IN_HEADER, description=" Please Provide Bearer JWT token", type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        user = request.user
        favorite_foods = FoodProduct.objects.filter(fvrt_by=user)
        serializer = FoodProductSerializer(favorite_foods, many=True)
        page = self.pagination_class().paginate_queryset(serializer.data, self.request)
        if page is not None:
            return self.pagination_class().get_paginated_response(page)
        if favorite_foods.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'You dont have any fvrt food'}, status=status.HTTP_404_NOT_FOUND)

class GetSpecialOffer(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(name = 'Authorization', in_=openapi.IN_HEADER, description="Please Provide Bearer JWT token", type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        try:
            food_ids = [food.id for food in FoodProduct.objects.all()]
            random_ids = random.sample(food_ids, min(3, len(food_ids)))
            foods = FoodProduct.objects.filter(pk__in=random_ids)
            serializer = FoodProductSerializer(foods, many=True)
            for data in serializer.data:
                off = round(float(data['price']) * random.randint(10, 30) / 100, 2)
                data['price'] = f"{float(data['price']) - off}"
                data['Note'] = f'You Get {off}% off On This Food'
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
