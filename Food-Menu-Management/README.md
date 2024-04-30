# Food Menu Management API

This repository contains the backend code for a Food Menu Management application. It provides RESTful APIs for user authentication, managing food products, adding favorites Foods, and retrieving special offers.

## Technologies Used

- Django: A high-level Python web framework for rapid development and clean, pragmatic design.
- Django REST Framework: A powerful and flexible toolkit for building Web APIs in Django.
- Simple JWT: Python package for easy JWT handling in Django REST Framework.

- PyYASG: Simplifies Swagger documentation for Django REST Framework.

- PostgreSQL: A powerful, open-source object-relational database system.

## Features

- User Authentication: Users can sign up, log in, and obtain JWT tokens for authentication.
- Food Product Management: Admin users can perform CRUD operations on food products,
and users can get list of food product
- Favorite Foods: Users can add and view their favorite food products.
- Special Offers: Users can view special offers randomly generated from available food products.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Akhtar21yr/Food-Menu-Management.git
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database according to settings in settings.py.
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Enter Your Database Name',
        'USER': 'Enter Your Username',
        'PASSWORD': 'Enter You Password',
        'HOST': 'localhost',  
    }
}
```

4. Apply migrations:
```bash 
py manage.py makemigrations
py manage.py migrate  
```
5. Run the development server:
```bash
python manage.py runserver
```

6. Run the following command to execute the test suite:
```bash
python manage.py test
```


## API Reference

#### User sign up

```http
  POST /api/sign-up/
```

#### User Login

```http
  POST /api/sign-in/
```

####  Retrieve list of food products or create a new food product.

```http
  GET /api/products/
```
```http
  POST /api/products/
```

#### Retrieve, update, or delete a specific food product.

```http
  GET /api/products/<int:pk>
```
```http
  PUT /api/products/<int:pk>
```
```http
  PATCH /api/products/<int:pk>
```
```http
  DELETE /api/products/<int:pk>
```

#### Add a food product to favorites.

```http
  POST /api/add-to-fvrt/<int:food_id>
```

#### Retrieve favorite food products.

```http
  GET /api/get-fvrt/
```

#### Retrieve special offers.

```http
  GET /api/get-offers/
```
#### See Swagger Documnataion.

## Swagger Documentation

Explore the API endpoints interactively using Swagger:

[Swagger Documentation](http://127.0.0.1:8000/swagger/)




