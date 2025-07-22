# HolbertonBnB (HBnB) – Part 3: Database Integration & Authentication

## Overview

**Part 3** of the AirBnB clone project brings full database integration and JWT authentication to the RESTful API. This phase transitions the application from in-memory data storage to a persistent SQLite backend with SQLAlchemy ORM, enabling robust data management, user authentication, and real-world deployment readiness.

The project follows a modular, layered architecture with clear separation of concerns between API, business logic, data persistence, and authentication layers.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- SQLite (included with Python standard library)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd holbertonschool-hbnb/part3/hbnb
   ```

2. **Set up a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix/MacOS:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Database Setup

1. **Initialize the database schema and seed data:**
   ```bash
   cd instance
   sqlite3 development.db < create_tables.sql
   sqlite3 development.db < insert_data.sql
   ```

### Running the Application

```bash
python run.py
```

- The API will be available at: `http://localhost:5000/`
- Interactive API docs (Swagger UI): `http://localhost:5000/`

---

## ✨ What's New in Part 3

- **🔐 JWT Authentication:** Secure user authentication with JSON Web Tokens
- **🗄️ Persistent Storage:** All data stored in SQLite database with SQLAlchemy ORM
- **✅ Data Validation:** SQLAlchemy validators for data integrity
- **🧪 Comprehensive Testing:** Automated test suite covering all endpoints
- **🔧 Production-Ready:** Modular architecture ready for scaling
- **📊 Database Schema:** Proper relationships and constraints

---

## 🏗️ Project Structure

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py           # Authentication endpoints
│   │       ├── amenities.py      # Amenities endpoints
│   │       ├── places.py         # Places endpoints
│   │       ├── reviews.py        # Reviews endpoints
│   │       └── users.py          # Users endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── amenity.py           # Amenity model with validation
│   │   ├── base_model.py        # Base model with common fields
│   │   ├── place.py             # Place model with validators
│   │   ├── review.py            # Review model with rating validation
│   │   └── user.py              # User model with password hashing
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── amenity_repository.py # Amenity data access
│   │   ├── place_repository.py   # Place data access
│   │   ├── repository.py         # Repository interface
│   │   ├── review_repository.py  # Review data access
│   │   └── user_repository.py    # User data access
│   └── services/
│       ├── __init__.py
│       ├── amenity_service.py   # Amenity business logic
│       ├── facade.py            # Facade pattern implementation
│       ├── place_service.py     # Place business logic
│       ├── review_service.py    # Review business logic
│       └── user_service.py      # User business logic
├── instance/
│   ├── create_tables.sql        # Database schema
│   ├── insert_data.sql          # Initial data seeding
│   ├── development.db           # SQLite database (auto-generated)
│   └── comprehensive_test_hbnb.sh # Complete test suite
├── config.py                    # Application configuration
├── requirements.txt             # Python dependencies
├── run.py                      # Application entry point
└── README.md
```

---

## 🔐 Authentication

### Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.io","password":"admin123"}'
```

### Using Authentication
```bash
curl -X GET http://localhost:5000/api/v1/users/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Default Admin User
- **Email:** admin@hbnb.io
- **Password:** admin123

---

## 🗄️ Database

- **Engine:** SQLite with SQLAlchemy ORM
- **File:** `instance/development.db`
- **Schema:** Defined in `instance/create_tables.sql`
- **Seeding:** Initial data in `instance/insert_data.sql`
- **Validation:** SQLAlchemy validators for data integrity

### Database Schema
- **Users:** Authentication, profiles, admin roles
- **Places:** Properties with location, pricing, amenities
- **Reviews:** User reviews with ratings (1-5)
- **Amenities:** Configurable features for places
- **Place-Amenity:** Many-to-many relationship

---

## 🧪 Testing

### Automated Test Suite
Run the comprehensive test suite:
```bash
cd instance
./comprehensive_test_hbnb.sh
```

This script tests:
- ✅ Authentication endpoints
- ✅ Users CRUD operations
- ✅ Amenities CRUD operations  
- ✅ Places CRUD operations
- ✅ Reviews CRUD operations
- ✅ Error handling (404, 401, 400)

### Manual Testing
Test the API using:
- **Swagger UI:** Available at `http://localhost:5000/`
- **cURL:** Command-line HTTP client
- **Postman:** GUI API testing platform

Example requests:
```bash
# Get all users
curl -X GET http://localhost:5000/api/v1/users/

# Create a place (requires authentication)
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Place","description":"A great place","price":100.0,"latitude":40.7128,"longitude":-74.0060}'
```

---

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/protected` - Test protected endpoint

### Users
- `GET /api/v1/users/` - List all users
- `POST /api/v1/users/` - Create new user (admin only)
- `GET /api/v1/users/{id}` - Get specific user
- `PUT /api/v1/users/{id}` - Update user (admin only)

### Places
- `GET /api/v1/places/` - List all places
- `POST /api/v1/places/` - Create new place (authenticated)
- `GET /api/v1/places/{id}` - Get specific place
- `PUT /api/v1/places/{id}` - Update place (owner only)

### Reviews
- `GET /api/v1/reviews/` - List all reviews
- `POST /api/v1/reviews/` - Create new review (authenticated)
- `GET /api/v1/reviews/{id}` - Get specific review
- `PUT /api/v1/reviews/{id}` - Update review (owner only)
- `DELETE /api/v1/reviews/{id}` - Delete review (owner only)
- `GET /api/v1/reviews/places/{place_id}/reviews` - Get reviews for a place

### Amenities
- `GET /api/v1/amenities/` - List all amenities
- `POST /api/v1/amenities/` - Create new amenity (admin only)
- `GET /api/v1/amenities/{id}` - Get specific amenity
- `PUT /api/v1/amenities/{id}` - Update amenity (admin only)

---

## 🔧 Dependencies

```txt
flask>=2.0.0          # Web framework
flask-restx>=1.0.0    # REST API extension with documentation
flask-sqlalchemy>=3.0.0  # SQLAlchemy integration
flask-jwt-extended>=4.5.0  # JWT authentication
bcrypt>=4.0.0         # Password hashing
```

---

## ✨ Features

### Core Functionality
- **🔐 JWT Authentication:** Secure user login with token-based sessions
- **👥 User Management:** Full CRUD with admin roles and password hashing
- **🏠 Place Management:** Properties with location, pricing, and amenities
- **⭐ Review System:** User reviews with rating validation (1-5)
- **🏷️ Amenity Management:** Configurable features for places

### Technical Features
- **🗄️ SQLAlchemy ORM:** Object-relational mapping with validation
- **✅ Data Validation:** SQLAlchemy validators for data integrity
- **🔄 Business Logic:** Service layer with proper separation of concerns
- **📊 Relationships:** Proper foreign keys and many-to-many associations
- **🧪 Testing:** Comprehensive automated test suite
- **📚 Auto-documentation:** Interactive Swagger/OpenAPI docs

---

## 🏛️ Architecture Patterns

- **🔐 Authentication Layer:** JWT-based security
- **🌐 API Layer:** RESTful endpoints with Flask-RESTx
- **🔧 Service Layer:** Business logic and operations
- **📊 Model Layer:** Data models with SQLAlchemy
- **💾 Repository Layer:** Data access abstraction
- **🗄️ Database Layer:** SQLite with SQLAlchemy ORM

---

## 🚀 Development

### Configuration
- Database: `instance/development.db`
- Debug mode: Enabled in development
- JWT secret: Configurable via environment variables

### File Structure
- **Models:** Data validation and relationships
- **Services:** Business logic and operations
- **API:** RESTful endpoints and serialization
- **Instance:** Database files and scripts (gitignored)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is part of the Holberton School curriculum.

---

## 👥 Authors

- [Clément Gibot](https://github.com/clementgibot25)
- [Arnaud Tilawat](https://github.com/TilawatArnaud)  
- [Maxime Naguet](https://github.com/Roupies)

---

**Status:** ✅ Production-ready with full database integration and authentication
