## commenting the code 
## study the notes provided sahil sir

# 🛒 Ecommerce Backend API

A FastAPI-powered backend service for an e-commerce platform, providing robust authentication, product management, and shopping cart functionality.

---

## Features

-  JWT Authentication (access + refresh tokens)
-  Role-based access: `admin`, `user`
-  Product CRUD (admin) and public listing with filters
-  Add, update, remove, and view cart items
-  Forgot/Reset password functionality
-  Strong validation using `EmailStr` and password rules
-  Domain-restricted signups (`gmail.com`, `yahoo.com`, `nucleusteq.org`)
-  Structured logging for all major operations

---

##  Tech Stack

- **FastAPI** + **Pydantic**
- **SQLAlchemy**
- **PostgreSQL / SQLite**
- **JWT** authentication
- **Uvicorn** for ASGI serving

---

## 📬 API Endpoints

###  Auth

 Method  Endpoint            Description              

1. POST   `/auth/signup`      Register a new user      
2. POST   `/auth/signin`      Login and get tokens     
3. POST   `/auth/forgot-password`  Request reset token 
4. POST   `/auth/reset-password`   Reset password      

### Products

 Method  Endpoint                 Description               

 GET     `/products/`             Get public product list   
 POST    `/admin/products`        Add product (admin only)  
 PUT     `/admin/products/{id}`   Update product (admin)    
 DELETE  `/admin/products/{id}`   Delete product (admin)    

### Cart

 Method  Endpoint                 Description                  

 GET     `/cart/`                 View user's cart             
 POST    `/cart/`                 Add product to cart          
 PATCH   `/cart/{product_id}`     Update quantity of cart item 
 DELETE  `/cart/{product_id}`     Remove item from cart        

---

## Validation Rules

### Email Validation

- Only emails from:
  - `gmail.com`
  - `yahoo.com`
  - `nucleusteq.org`

### Password Validation

- Minimum 8 characters
- Must include:
  - At least one uppercase letter
  - At least one digit
  - At least one special character from `!@#$%^&*`

---

## ⚙️ Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/Aayush8730/ecommerce_backend-FastAPI
cd ecommerce-backend


2. Activate a virtual environment

python -m venv venv
source venv/bin/activate  


3. Install Dependencies
pip install -r requirements.txt


4. Create .env file
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce
SECRET_KEY=your_jwt_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7


5. Run the server
uvicorn app.main:app --reload


