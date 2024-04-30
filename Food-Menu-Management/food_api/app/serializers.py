from rest_framework import serializers
from .models import User, FoodProduct, Customization


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'password2','age','city']

    def validate(self, data):
        if data['password'] != data['password2']:
             raise serializers.ValidationError({'password': 'Passwords do not match'})
        
        return data

    def create(self, data):
        password = data.pop('password2', '')
        user = User.objects.create(**data)
        user.set_password(password)
        user.save()
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email','password']



class CustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customization
        fields = ['id', 'name', 'group', 'toppings']
        read_only_fields = ['id']

class FoodProductSerializer(serializers.ModelSerializer):
    customizations = CustomizationSerializer(many=True)

    class Meta:
        model = FoodProduct
        fields = ['id', 'name', 'description', 'price', 'average_rating', 'category', 'product_type','customizations']
        read_only_fields = ['id','fvrt']

    def create(self, validated_data):
        customization_data = validated_data.pop('customizations')
        food_product = FoodProduct.objects.create(**validated_data)

        for customization_item in customization_data:
            Customization.objects.create(food_product=food_product, **customization_item)

        return food_product

    def update(self, instance, validated_data):
        customizations_data = validated_data.pop('customizations', None)
        if customizations_data is not None:
            instance.customizations.all().delete()
            for customization_data in customizations_data:
                Customization.objects.create(food_product=instance, **customization_data)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.average_rating = validated_data.get('average_rating', instance.average_rating)
        instance.category = validated_data.get('category', instance.category)
        instance.product_type = validated_data.get('product_type', instance.product_type)
        instance.save()

        return instance
    
