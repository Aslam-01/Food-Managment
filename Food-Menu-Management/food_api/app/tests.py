from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import FoodProduct, User
from rest_framework.test import force_authenticate

class UserSignupViewTestCase(APITestCase):
    """
    Test case for the UserSignupView class.
    """

    def test_user_signup_success(self):
        """
        Test user signup with valid data.
        """
        url = 'http://127.0.0.1:8000/api/sign-up/'
        data = {
            "email": "test@example.com",
            "full_name": "John Doe",
            "password": "testpassword",
            "password2": "testpassword",
            "age": 30,
            "city": "New York"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('msg', response.data)
        self.assertEqual(response.data['msg'], 'Register Successful')

    def test_user_signup_failure(self):
        """
        Test user signup with invalid data.
        """
        url = 'http://127.0.0.1:8000/api/sign-up/'
        data = {
            # adding invalid email
            "email": "",  
            "full_name": "John Doe",
            "password": "testpassword",
            "password2": "testpassword",
            "age": 30,
            "city": "New York"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)  


class UserLoginViewTestCase(APITestCase):
    """
    Test case for the UserLoginView class.
    """

    def setUp(self):
        """
        Create a test user for login testing.
        """
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
            full_name="John Doe",
            city="New York",
            age=30
        )

    def test_user_login_success(self):
        """
        Test user login with correct credentials.
        """
        url = 'http://127.0.0.1:8000/api/sign-in/'
        data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('msg', response.data)
        self.assertEqual(response.data['msg'], 'Login Successful')

    def test_user_login_failure(self):
        """
        Test user login with incorrect credentials.
        """
        url = 'http://127.0.0.1:8000/api/sign-in/'

        # giving wrong details
        data = {
            "email": "test@example.com",
            "password": "wrongpassword"  
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('errors', response.data)
        self.assertIn('validation_erros', response.data['errors'])
        self.assertIn('password and email is not valid', response.data['errors']['validation_erros'])


class FoodProductTests(APITestCase):

    """
    Test class for testing Food Product related activities.

    Methods:
        - test_get_food_product_list: Test case for retrieving a list of food products.
        - test_get_food_product_detail: Test case for retrieving details of a specific food product.
        - test_create_food_product: Test case for creating a new food product.
        - test_update_food_product: Test case for updating an existing food product.
        - test_partial_update_food_product: Test case for partially updating an existing food product.
        - test_delete_food_product: Test case for deleting an existing food product.
        - test_add_favorite_food: Test case for adding a food product to favorites.
        - test_get_favorite_food: Test case for retrieving favorite food products.
        - test_get_offers: Test case for retrieving special offers.
    """

    def setUp(self):
        """
        Create some initial data for testing
        """
        self.food_product_data = {
            "name": "Test Food",
            "description": "Test description",
            "price": "10.00",
            "average_rating": "4.5",
            "category": "Test category",
            "product_type": "Veg",
        }
        self.food_product = FoodProduct.objects.create(**self.food_product_data)
        self.user = User.objects.create_user(
            email="my@email.com",
            password="password123",
            full_name="akhtra",
            city="mumbai",
            age=21,
            is_admin = True
        )

    def test_get_food_product_list(self):
        """
        Test retrieving a list of food products.
        """

        url = "http://127.0.0.1:8000/api/products/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_food_product_detail(self):
        """
        Test retrieving details of a specific food product.
        """

        url = f"http://127.0.0.1:8000/api/products/{self.food_product.pk}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_food_product(self):
        """
        Test creating a new food product.
        """

        url = reverse("products")
        data = {
            "id": 7,
            "name": "Sushi",
            "description": "Traditional Japanese sushi rolls",
            "price": "15.99",
            "average_rating": 4.7,
            "category": "Japanese",
            "product_type": "NonVeg",
            "customizations": [
                {
                    "id": 11,
                    "name": "Assorted Fish",
                    "group": "Fillings",
                    "toppings": "Salmon, Tuna, Shrimp",
                },
                {
                    "id": 12,
                    "name": "Wasabi",
                    "group": "Condiments",
                    "toppings": "Wasabi Paste",
                },
            ],
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('msg', response.data)
        self.assertEqual(response.data['msg'], f'{data['name']} Is Added Successfully')

    def test_update_food_product(self):
        """
        Test updating an existing food product.
        """

        url = f"http://127.0.0.1:8000/api/products/{self.food_product.pk}"
        data = {
            "name": "Updated Food",
            "description": "Updated description",
            "price": "12.00",
            "average_rating": "4.7",
            "category": "Updated category",
            "product_type": "NonVeg",
            "customizations": [
                {
                    "id": 11,
                    "name": "Assorted Fish",
                    "group": "Fillings",
                    "toppings": "Salmon, Tuna, Shrimp",
                },
                {
                    "id": 12,
                    "name": "Wasabi",
                    "group": "Condiments",
                    "toppings": "Wasabi Paste",
                },
            ],
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('msg', response.data)
        self.assertEqual(response.data['msg'], f'{data['name']} is updated')

    def test_partial_update_food_product(self):
        """
        Test partially updating an existing food product.
        """

        url = f"http://127.0.0.1:8000/api/products/{self.food_product.pk}"
        data = {
            "name": "Updated Food",
            "description": "Updated description",
            "price": "12.00",
            "average_rating": "4.7",
            "product_type": "NonVeg",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('msg', response.data)
        self.assertEqual(response.data['msg'], f'{data['name']} is updated')

    def test_delete_food_product(self):
        """
        Test deleting an existing food product.
        """

        url = f"http://127.0.0.1:8000/api/products/{self.food_product.pk}"
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('msg', response.data)

    def test_add_favorite_food(self):
        """
        Test adding a food product to favorites.
        """

        url = f"http://127.0.0.1:8000/api/add-to-fvrt/{self.food_product.pk}"
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('msg', response.data)

    def test_get_favorite_food(self):
        """
        Test retrieving favorite food products.
        """

        url = "http://127.0.0.1:8000/api/get-fvrt/"
        self.client.force_authenticate(user=self.user)
        self.test_add_favorite_food()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_get_offers(self):
        """
        Test retrieving special offers.
        """

        url = "http://127.0.0.1:8000/api/get-offers/"
        self.client.force_authenticate(user=self.user)
        for _ in range(3):
            self.test_create_food_product()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

