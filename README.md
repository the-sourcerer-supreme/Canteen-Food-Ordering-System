# VITEats – Online Food Ordering System

A web-based food ordering platform developed using Django that allows users to browse menu items, add food to a cart, place orders, and track order status. The system also includes product ratings, reviews, and a quick description modal for a better user experience.

This project simulates a digital canteen ordering system for college environments, enabling students to order food online instead of waiting in queues.

## Project Overview

Traditional college canteens often face problems such as long queues, order confusion, and inefficient manual tracking. This system provides a centralized online ordering platform where users can view food items, place orders, and track their status digitally.

The application is built using Python, Django, HTML, CSS, JavaScript, and SQLite for database management.

## Key Features

### 1. User Authentication

- **Secure signup and login system**

- **Authentication handled using Django’s built-in authentication system**

- **Automatic customer profile creation using signals**

### 2. Product Menu System

Users can:

- **Browse food items available in the canteen**

- **View product images, prices, and ratings**

- **Access quick product descriptions through a popup modal**

### 3. Shopping Cart System

- **Add or remove items from the cart**

- **Quantity adjustment**

- **Dynamic cart updates using JavaScript**

Cart works for:

- **Logged-in users (database storage)**

- **Guest users (cookie-based storage)**

### 4. Rating and Review System

Users can:

- **Rate food items using a 1–5 star rating**

- **Submit written reviews**

- **View average ratings displayed on the store page**

### 5. Order Management

- **Place orders through a checkout system**

- **Orders stored in the database**

- **Automatic order total calculation**

### 6. Order Tracking

Users can:

- **View previous orders**

- **Track order status**

```Order status flow:

Pending → Paid → Preparing → Ready → Delivered
```

### 7. Product Search

Users can search menu items by name using a simple search functionality.

### 8. Quick Description Modal

A popup modal allows users to quickly view product descriptions without navigating away from the store page.

### 9. Automated Setup Scripts

PowerShell scripts are included to automate:

- **virtual environment creation**

- **dependency installation**

- **migrations**

- **server startup**

## Technology Stack

### Backend

- **Django**

- **Python**

### Frontend

- **HTML**

- **CSS**

- **JavaScript**

- **Bootstrap**

### Database

- **SQLite (default Django database)**

## Project Structure
```
VITEats
│
├── HomeFood/           # Django project configuration
├── scripts/            # Main application
│   ├── setup.ps1       # Automated setup script
│   └── run.ps1         # Run server script
├── static/             # CSS, JS, Images
├── store/              # Main application   
│   ├── admin.py        # admin config
│   ├── models.py       # Database models
│   ├── views.py        # Application logic
│   ├── urls.py         # URL routing
│   ├── utils.py        # Cart and guest user utilities
│   └── signals.py      # Auto customer profile creation
├── templates/
│   └── store/
│       ├── store.html
│       ├── cart.html
│       ├── checkout.html
│       └── product_detail.html
└── manage.py
```

## Installation Guide
### 1. Clone the Repository
```
git clone https://github.com/the-sourcerer-supreme/VITEats.git
cd VITEats
```

### 2. 
```powershell
cd c:\VITEats
Set-ExecutionPolicy -Scope Process Bypass
```

### 3. Run setup script
```
.\scripts\setup.ps1
```

### 4. Run server script
```
.\scripts\run.ps1
```

#### Open the application:

- **Site**: `http://127.0.0.1:8000/`
- **Store/Menu**: `http://127.0.0.1:8000/store/`
- **My Orders**: `http://127.0.0.1:8000/orders/`
- **Admin**: `http://127.0.0.1:8000/admin/`

## What the scripts do

- `scripts/setup.ps1`
  - Creates `.venv/`
  - Upgrades pip
  - Installs dependencies
  - Runs `python manage.py check`
  - Runs `python manage.py migrate`

- `scripts/run.ps1`
  - Starts the dev server via `python manage.py runserver`

> Note: `setup.ps1` writes a temporary “pip-safe” requirements file before installing. This is intentional (avoids Windows encoding issues that can break `pip -r requirements.txt`).

## Creating an admin user (superuser)

```powershell
cd c:\VITEats
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Then login at `http://127.0.0.1:8000/admin/`.

### Reset database (start fresh)

This project uses SQLite. If you want a clean DB:

1. Stop the server
2. Delete `db.sqlite3`
3. Run migrations again:

```powershell
cd c:\VITEats
.\.venv\Scripts\python.exe manage.py migrate
```

### Note: Please Setup Payment account before proceeding with any payment transactions on this project.

## Possible improvements include:

- **Online payment gateway integration**

- **Real-time order status notifications**

- **Admin dashboard analytics**

- **Mobile application version**

- **Recommendation system for food items**

- **Inventory management for canteen staff**

## Educational Purpose

This project was developed as part of a web development and software engineering learning exercise to demonstrate practical implementation of:
- **Django web framework**
- **database modeling**
- **authentication systems**
- **dynamic cart management**
- **rating and review mechanisms**
