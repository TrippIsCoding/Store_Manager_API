# E-Commerce Multi-API System

A microservices-based e-commerce platform built with FastAPI, featuring separate APIs for inventory management and user operations.

## Architecture

This project implements a microservices architecture with two independent APIs:

- **Manager API**: Handles inventory management (CRUD operations)
- **User API**: Manages user authentication and shopping cart functionality

Both APIs share a PostgreSQL database and the User API uses Redis for cart storage.

## Live Deployment

- **Manager API**: https://store-manager-api.onrender.com/docs
- **User API**: https://store-user-api.onrender.com/docs

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **Authentication**: JWT tokens
- **Password Hashing**: bcrypt
- **Deployment**: Render

## API Endpoints

### Manager API (/inventory)
- `GET /view` - Get all inventory items
- `POST /add` - Add new item
- `PUT /update/{id}` - Update item price and stock
- `DELETE /delete/{id}` - Remove item

### User API
**Authentication (/auth)**
- `POST /user/signup` - Create account
- `POST /user/login` - Login and receive JWT token

**Customer Operations (/customer)**
- `GET /view/store` - Browse items
- `POST /cart/add/{id}` - Add item to cart (auth required)
- `GET /cart/view` - View cart (auth required)
- `DELETE /cart/delete/{id}` - Remove item from cart (auth required)

## Local Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with database and Redis credentials
4. Run Manager API: `uvicorn Manager_API.main:app --reload --port 8000`
5. Run User API: `uvicorn User_API.main:app --reload --port 8001`

## Key Features

- JWT authentication with 30-minute expiration
- Bcrypt password hashing
- Redis-based shopping cart with 24-hour expiration
- Input validation with Pydantic
- Comprehensive error handling
- Interactive API documentation at `/docs`