# HolbertonBnB - Console

Welcome to the HolbertonBnB project! This is a command-line interface (CLI) for managing AirBnB-like objects, built with Python.

## Project Structure

```
hbnb/
├── app/                    # Main application package
│   ├── __init__.py         # Package initialization
│   │
│   ├── api/               # API endpoints
│   │   ├── __init__.py
│   │   └── v1/             # API version 1
│   │       ├── __init__.py
│   │       ├── amenities.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── users.py
│   │
│   ├── models/            # Data models
│   │   ├── __init__.py
│   │   ├── amenity.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── user.py
│   │
│   ├── persistence/       # Data persistence layer
│   │   ├── __init__.py
│   │   ├── memory_amenity_repository.py
│   │   ├── memory_place_repository.py
│   │   ├── memory_review_repository.py
│   │   ├── memory_user_repository.py
│   │   └── repository.py
│   │
│   └── services/          # Business logic
│       ├── __init__.py
│       ├── amenity_service.py
│       ├── facade.py
│       ├── place_service.py
│       ├── review_service.py
│       └── user_service.py
│
├── config.py              # Application configuration
├── requirements.txt        # Python dependencies
└── run.py                 # Application entry point
```

## Getting Started

### Prerequisites

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