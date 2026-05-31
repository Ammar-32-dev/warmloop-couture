# E-commerce Django Application

## Overview
This is a simple e-commerce web application built with Django. It allows users to browse products, view product details, and manage a shopping cart.

## Features
- Product listing page
- Product detail page
- Shopping cart functionality using Django sessions
- Responsive design with CSS styling
- Modular template structure with separate header and footer

## Prerequisites
- Python 3.8 or higher
- Django 5.2.4 or higher

## Installation
1. Create a virtual environment:
   ```
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source .venv/bin/activate
     ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```
   python manage.py runserver
   ```

5. Open your browser and navigate to `http://127.0.0.1:8000/`

## Application Structure
- `myapp`: Main application for product management
- `cart`: Shopping cart functionality
- `templates`: HTML templates
- `static`: CSS stylesheets and images

## URLs
- `/` - Product listing page
- `/product/<id>/` - Product detail page
- `/cart/` - Shopping cart page
- `/cart/add/<id>/` - Add product to cart
- `/cart/remove/<id>/` - Remove product from cart
- `/cart/update/<id>/` - Update product quantity in cart

## How to Use
1. Browse products on the homepage
2. Click on a product to view its details
3. Add products to your cart using the "Add to Cart" button
4. View and manage your cart through the cart icon in the header
5. Update quantities or remove items from the cart as needed
