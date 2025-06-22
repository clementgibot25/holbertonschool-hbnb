# HolbertonBnB (HBnB) – Part 2: API & Business Logic

This project implements the core API and business logic for a simplified AirBnB clone using Python, Flask, and Flask-RESTx. It is organized in a modular, scalable way to separate presentation, business, and persistence layers, and prepares for future extensions like database integration and authentication.

---

## Project Structure

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── amenities.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── users.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── amenity.py
│   │   ├── base_model.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── user.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── in_memory_repository.py
│   │   └── repository.py
│   └── services/
│       ├── __init__.py
│       ├── amenity_service.py
│       ├── facade.py
│       ├── place_service.py
│       ├── review_service.py
│       └── user_service.py
│   └── tests/
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

### Key Layers
- **API (Presentation Layer)**: `app/api/v1/` – Defines RESTful endpoints for Users, Places, Reviews, and Amenities using Flask-RESTx.
- **Business Logic (Services Layer)**: `app/services/` – Core logic for entity management and the Facade pattern for orchestrating operations.
- **Models**: `app/models/` – Data models for User, Place, Review, Amenity, and a BaseModel for shared fields.
- **Persistence Layer**: `app/persistence/` – In-memory repository for storing objects (ready for future DB integration).

---

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd holbertonschool-hbnb/part2/hbnb
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
To start the Flask API server:
```bash
python run.py
```
- The API will be available at `http://localhost:5000/`
- Swagger/OpenAPI documentation is auto-generated at `/` (root URL)

---

## Project Vision & Scope
This part focuses on implementing the Presentation and Business Logic layers:
- **Presentation Layer**: RESTful API endpoints for CRUD operations on Users, Places, Reviews, and Amenities.
- **Business Logic Layer**: Core classes, relationships, and validation using the Facade pattern.
- **Persistence**: In-memory storage (will be replaced by a database in the next part).
- **No authentication/authorization yet** – code is modular to allow easy integration in the future.

### Main Features
- Modular, scalable Python project structure
- RESTful API for managing Users, Places, Reviews, Amenities
- Data serialization: endpoints return extended/nested attributes (e.g., place owner details, amenities)
- Input validation and error handling
- Facade pattern for clean separation between API and business logic
- Ready for database integration and authentication in future phases

---

## How It Works
- **API Endpoints**: Defined in `app/api/v1/` using Flask-RESTx for documentation and validation
- **Business Logic**: Service classes in `app/services/` implement all core operations and orchestrate relationships
- **Persistence**: All objects are stored in-memory via the repository pattern
- **Testing**: You can use cURL, Postman, or Swagger UI to test endpoints

---

## Recommended Resources
- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/en/latest/)
- [REST API Best Practices](https://restfulapi.net/)
- [Python Project Structure Guide](https://docs.python-guide.org/writing/structure/)
- [Facade Pattern in Python](https://refactoring.guru/design-patterns/facade/python/example)

---

## Next Steps
- Part 3: Add database-backed persistence (SQLAlchemy)
- Add JWT authentication and role-based access control
- Expand testing suite and CI/CD integration

---

## Authors
- [Your Name Here]
- Project inspired by Holberton School curriculum
- Python 3.8 or higher
- pip (Python package installer)

### Installation
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd holbertonschool-hbnb/part2/hbnb
   ```

2. **Set up a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the application by running:

```bash
python run.py
```

## Dependencies

- `flask` - Web framework
- `flask-restx` - Extension for building REST APIs with Flask

All dependencies are listed in `requirements.txt`.

## Features

- Manage AirBnB-like objects (Users, Places, Amenities, Reviews)
- In-memory data persistence
- RESTful API endpoints

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is part of the Holberton School curriculum.