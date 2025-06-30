# HolbertonBnB (HBnB) – Part 2: API & Business Logic

A simplified AirBnB clone implementing RESTful API and business logic using Python, Flask, and Flask-RESTx. This project features a modular, scalable architecture that separates presentation, business, and persistence layers, preparing for future database integration and authentication.

---

## 🏗️ Project Architecture

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── amenities.py      # Amenities endpoints
│   │       ├── places.py         # Places endpoints
│   │       ├── reviews.py        # Reviews endpoints
│   │       └── users.py          # Users endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── amenity.py           # Amenity model
│   │   ├── base_model.py        # Base model with common fields
│   │   ├── place.py             # Place model
│   │   ├── review.py            # Review model
│   │   └── user.py              # User model
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── in_memory_repository.py  # In-memory storage implementation
│   │   └── repository.py            # Repository interface
│   ├── services/
│   │   ├── __init__.py
│   │   ├── amenity_service.py   # Amenity business logic
│   │   ├── facade.py            # Facade pattern implementation
│   │   ├── place_service.py     # Place business logic
│   │   ├── review_service.py    # Review business logic
│   │   └── user_service.py      # User business logic
│   └── tests/                   # Test files
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── run.py                      # Application entry point
└── README.md
```

### 🎯 Layered Architecture

- **🌐 API Layer** (`app/api/v1/`): RESTful endpoints with Flask-RESTx for automatic documentation
- **🏛️ Facade Layer** (`app/services/facade.py`): Unified interface orchestrating all business operations
- **🔧 Business Logic** (`app/services/`): Core business operations and individual service classes
- **📊 Models** (`app/models/`): Data models with validation and relationships
- **💾 Persistence** (`app/persistence/`): Repository pattern with in-memory storage

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd holbertonschool-hbnb/part2/hbnb
   ```

2. **Set up virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python run.py
```

The API will be available at:
- **API Base URL**: `http://localhost:5000/`
- **Interactive Documentation**: `http://localhost:5000/` (Swagger UI)

---

## ✨ Features

### Core Functionality
- **User Management**: Create, read, update users with email validation
- **Place Management**: Properties with location, pricing, and amenities
- **Review System**: User reviews with ratings for places
- **Amenity Management**: Configurable amenities for places

### Technical Features
- **RESTful API Design**: Clean, consistent endpoint structure
- **Data Serialization**: Extended responses with nested relationships
- **Input Validation**: Comprehensive data validation and error handling
- **Modular Architecture**: Easy to extend and maintain
- **Auto-generated Documentation**: Interactive Swagger/OpenAPI docs

### API Endpoints Overview
- `GET/POST/PUT /api/v1/users/` - User management (create, read, update)
- `GET/POST/PUT /api/v1/places/` - Place management (create, read, update)
- `GET/POST/PUT/DELETE /api/v1/reviews/` - Review management (full CRUD operations)
- `GET/POST/PUT /api/v1/amenities/` - Amenity management (create, read, update)

---

## 🔧 Dependencies

```txt
flask>=2.0.0          # Web framework
flask-restx>=1.0.0    # REST API extension with documentation
```

All dependencies are listed in `requirements.txt`.

---

## 🧪 Testing

You can test the API using:
- **Swagger UI**: Available at the root URL when running the application
- **cURL**: Command-line HTTP client
- **Postman**: API testing platform
- **HTTPie**: User-friendly command-line HTTP client

Example cURL request:
```bash
curl -X GET http://localhost:5000/api/v1/users/
```

---

## 🎯 Project Vision

This implementation focuses on the **Presentation** and **Business Logic** layers:

### Current Phase (Part 2)
- ✅ RESTful API with comprehensive CRUD operations
- ✅ Business logic with proper validation and relationships
- ✅ In-memory persistence with repository pattern
- ✅ Modular architecture ready for scaling

### Future Phases
- 🔄 **Part 3**: Database integration with SQLAlchemy
- 🔄 **Part 4**: JWT authentication and authorization

---

## 🏛️ Design Patterns

- **Facade Pattern**: Simplifies complex business operations
- **Repository Pattern**: Abstracts data access layer
- **Service Layer**: Separates business logic from presentation
- **Model-View-Controller**: Clear separation of concerns

---

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/en/latest/)
- [REST API Best Practices](https://restfulapi.net/)
- [Python Project Structure Guide](https://docs.python-guide.org/writing/structure/)
- [Facade Pattern in Python](https://refactoring.guru/design-patterns/facade/python/example)

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

- [Clément Gibot](https://github.com/clementgibot25)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Badge](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/clementgibot25)
- [Arnaud Tilawat](https://github.com/TilawatArnaud)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Badge](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/TilawatArnaud)
- [Maxime Naguet](https://github.com/Roupies)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Badge](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/Roupies)

---
