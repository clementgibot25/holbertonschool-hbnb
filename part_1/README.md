# System Design Diagrams

This directory contains several diagrams illustrating the architecture and key processes of the HBNB project. These diagrams are created using Mermaid.js and describe the data model and interactions between different components of the system.

## Introduction

This collection of system design diagrams aims to provide a clear, visual understanding of the HBNB project's internal structure and key workflows. Created using Mermaid.js, these diagrams are essential forls anyone looking to grasp:

*   The overall organization of the codebase.
*   The main data models and how they relate to each other.
*   Typical user interactions with the system.
*   Backend processing flows and critical decision logic.
*   Interactions between different architectural layers, such as the Presentation Layer, Business Logic Layer, and Database Layer.

Each diagram is accompanied by a detailed explanation to ensure clarity and provide necessary context, making this documentation valuable for contributors, reviewers, and developers new to the project.

## Diagrams Overview

The following diagrams are included:
1.  **`Package_diagram.svg`**: A **Package Diagram** that provides a high-level structural view of the HBNB application architecture. It organizes the system into distinct layers that encapsulate different responsibilities. This architectural pattern promotes modularity, scalability, and maintainability.
2.  **`business_logic_layer.md`**: A **Class Diagram** that outlines the main data models (entities) of the application, their attributes, methods, and relationships.
3.  **`fetch_places_diagram.md`**: A **Sequence Diagram** detailing the process of a user searching for and fetching a list of places.
4.  **`place_creation_diagram.md`**: A **Sequence Diagram** illustrating the workflow for a user creating a new place.
5.  **`register_user_diagram.md`**: A **Sequence Diagram** showing the steps involved in registering a new user.
6.  **`submit_review_diagram.md`**: A **Sequence Diagram** describing the process for a user submitting a review for a place and an administrator validating that review.

## Detailed Explanations

### 1. Package Diagram

![Package Diagram](Package_diagram.svg)

This Package Diagram visually represents the structural organization of the HBNB application at a global level. By grouping components into layers with clearly defined responsibilities, this architectural design enhances modularity, adaptability, and maintainability.

#### Components

The architecture is divided into three main layers, each containing packages (modules) responsible for specific aspects of the system:

**Presentation Layer**

*   **Purpose**: Interface between the user and the system.
*   **Responsibilities**:
    *   Handle user input/output.
    *   Validate input before passing it to the business layer.
    *   Act as a façade that hides the complexity of the underlying logic.
*   **Packages**:
    *   User Interface: Provides views, forms, and interaction points for the end-user (CLI, web interface, etc.).
    *   Services/API: RESTful endpoints or service classes that handle HTTP requests and prepare data for presentation.

**Business Logic Layer**

*   **Purpose**: Encapsulates the core functionality of the system.
*   **Responsibilities**:
    *   Process requests from the presentation layer.
    *   Coordinate business rules and workflows.
    *   Serve as the middle tier connecting the user interface and data access.
*   **Packages (Entities)**:
    *   User: Manages user-related operations (registration, login, etc.).
    *   Place: Handles listings, location data, and place management.
    *   Amenity: Represents available features for places.
    *   Review: Manages user reviews, ratings, and validation logic.
*   **Pattern Used**: Implements the Facade Pattern, providing a simplified interface to the complex business logic.

**Persistence Layer**

*   **Purpose**: Handles data storage and retrieval.
*   **Responsibilities**:
    *   Interact with the database (ORM or raw SQL).
    *   Encapsulate all low-level data operations.
*   **Package**:
    *   Database Access: Module responsible for CRUD operations, managing connections, and querying the data store.

### 2. Business Logic Layer

<img src="./business_logic_layer.png" alt="Business Logic Layer" width="463"/>

This class diagram provides a high-level view of the core entities in the HBNB system.

*   **Purpose**: To define the structure of the data, including the properties of each entity and how they relate to one another.
*   **Key Entities**:
    *   `BaseModel`: An abstract base class providing common attributes like `Unique_ID`, `creation_time`, and `update_time`, along with basic CRUD methods (`create`, `update`, `delete`, `listed`).
    *   `User`: Represents a user of the system. Inherits from `BaseModel`. Attributes include `first_name`, `last_name`, `email`, `password` (private), `is_admin`, and `is_owner`. It has a `register()` method.
    *   `Place`: Represents a property listing. Inherits from `BaseModel`. Attributes include `title`, `description`, `price`, location details (`latitude`, `longitude`, `city`, `state`), and `amenities` (protected list). Methods include `review_list()` (protected) and `get_average_rating()`.
    *   `Amenity`: Represents an amenity that a place can offer (e.g., Wi-Fi, pool). Inherits from `BaseModel`. Attributes include `name` and `description`.
    *   `Review`: Represents a review written by a user for a place. Inherits from `BaseModel`. Attributes include `rating`, `comment`, `author` (User), `for_place` (Place), and `approved` (private boolean). It has a private `approved_by_admin()` method.
*   **Relationships**:
    *   `User`, `Place`, `Amenity`, and `Review` all inherit from `BaseModel`.
    *   A `User` can own zero or more `Place`s (composition relationship).
    *   A `Place` can offer zero or more `Amenity`s, and an `Amenity` can be offered by multiple `Place`s (many-to-many).
    *   A `User` can write zero or more `Review`s (one-to-many).
    *   A `Place` can have zero or more `Review`s (one-to-many).
*   **Notes**:
    *   `BaseModel` is abstract.
    *   Users can be regular users or administrators.
    *   Each Place is owned by one User (composition relationship).
    *   Reviews are linked to both a User (author) and a Place.

### 3. Fetch Places Diagram

![Fetch Places Diagram](https://www.mermaidchart.com/raw/87e50b04-dc5a-4f06-a7ad-0f907c017e92?theme=dark&version=v0.1&format=svg)

This sequence diagram illustrates the interactions when a user searches for places.

*   **Purpose**: To show the flow of control and data as a user requests a list of places based on search criteria.
*   **Actors**:
    *   `User`: The end-user initiating the search.
    *   `Presentation`: The layer handling incoming requests and formatting responses (e.g., API endpoints).
    *   `BusinessLogic`: The layer containing the core application logic and validation.
    *   `Database`: The persistence layer where place data is stored.
*   **Key Steps**:
    1.  `User` sends a `GET /place` request with search criteria to the `Presentation` layer.
    2.  `Presentation` layer validates the format of the search criteria.
        *   If invalid, returns a `400 Bad Request`.
    3.  If valid, `Presentation` forwards the request to the `BusinessLogic` layer.
    4.  `BusinessLogic` layer validates the search criteria (e.g., criteria count > 0).
        *   If invalid, returns a `400 Bad Request`.
    5.  If valid, `BusinessLogic` requests the `Database` to fetch places matching the criteria.
    6.  `Database` attempts to retrieve the data.
        *   If a database error occurs (e.g., connection issue), it returns an error to `BusinessLogic`, which then results in a `500 Internal Server Error` to the `User`.
    7.  If successful, `Database` returns a list of places (or an empty list) to `BusinessLogic`.
    8.  `BusinessLogic` processes the result:
        *   If no places are found, it informs `Presentation`, which returns a `200 OK` with an empty list/message to the `User`.
        *   If places are found, it returns the list to `Presentation`, which then sends a `200 OK` with the list of places to the `User`.

### 4. Place Creation Diagram

![Place Creation Diagram](https://www.mermaidchart.com/raw/4177e42c-0402-47d5-9683-81c4f0fb2347?theme=dark&version=v0.1&format=svg)

This sequence diagram details the process of a user creating a new place.

*   **Purpose**: To outline the steps involved from the user initiating the creation of a place to its persistence in the database.
*   **Actors**: `User`, `Presentation`, `BusinessLogic`, `Database`.
*   **Key Steps**:
    1.  `User` first request a list of available amenities via `GET /amenities`. This involves `Presentation` -> `BusinessLogic` -> `Database` and back to display options to the user.
    2.  `User` sends a `POST /places` request with place data (title, description, price, location, selected amenities) to `Presentation`.
    3.  `Presentation` layer validates the format of the input data.
        *   If invalid, returns a `400 Bad Request`.
    4.  If valid, `Presentation` forwards the data to `BusinessLogic`.
    5.  `BusinessLogic` layer checks if a similar place already exists by querying the `Database` (e.g., based on title, latitude, longitude).
    6.  `Database` responds:
        *   If a similar place is found, `BusinessLogic` informs `Presentation`, which returns a `409 Conflict` to the `User`.
        *   If the place is not found (it's unique):
            1.  `BusinessLogic` instructs `Database` to insert the new place data.
            2.  `Database` attempts to save the new place.
                *   If a database error occurs, it results in a `500 Internal Server Error` to the `User`.
                *   If successful, `Database` returns a success status and the new Place ID to `BusinessLogic`.
            3.  `BusinessLogic` informs `Presentation`, which returns a `201 Created` status with the Place ID to the `User`.

### 5. Register User Diagram

![Register User Diagram](https://www.mermaidchart.com/raw/99ed0ffa-ad3a-4f45-a24e-6f2c3c966b26?theme=dark&version=v0.1&format=svg)

This sequence diagram shows the workflow for new user registration.

*   **Purpose**: To illustrate the sequence of events when a new user signs up for the service.
*   **Actors**: `User`, `Presentation`, `BusinessLogic`, `Database`.
*   **Key Steps**:
    1.  `User` sends a `POST` request with registration data (first_name, last_name, email, password) to `Presentation`.
    2.  `Presentation` layer validates the format of the registration data.
        *   If invalid (e.g., missing fields, invalid email format), returns a `400 Bad Request`.
    3.  If valid, `Presentation` forwards the data to `BusinessLogic`.
    4.  `BusinessLogic` layer checks if the provided email already exists by querying the `Database`.
    5.  `Database` responds:
        *   If the email already exists, `BusinessLogic` informs `Presentation`, which returns a `409 Conflict` to the `User`.
        *   If the email does not exist:
            1.  `BusinessLogic` instructs `Database` to save the new user.
            2.  `Database` attempts to create the new user entry.
                *   If a database error occurs, it results in a `500 Internal Server Error` to the `User`.
                *   If successful, `Database` returns a success status to `BusinessLogic`.
            3.  `BusinessLogic` informs `Presentation`, which returns a `201 Created` status to the `User`.

### 6. Submit Review Diagram

![Submit Review Diagram](https://www.mermaidchart.com/raw/e956318a-7745-47f7-bf13-b9b9f9dbca5f?theme=dark&version=v0.1&format=svg)

This sequence diagram covers two related processes: a user submitting a review for a place, and an administrator validating that review.

*   **Purpose**: To show the flow for creating new reviews and their subsequent approval.
*   **Actors**: `User` (can be a regular user or an Admin), `Presentation`, `BusinessLogic`, `Database`.
*   **Key Steps - Submitting a Review**:
    1.  `User` sends a `POST /reviews` request with review data (username, review_text, place ID, date) to `Presentation`.
    2.  `Presentation` layer validates the input (e.g., text length, date not in the future).
        *   If invalid, returns a `400 Bad Request`.
    3.  If valid, `Presentation` forwards the data to `BusinessLogic`.
    4.  `BusinessLogic` layer checks if the user has already submitted an identical review for the same place on the same date by querying the `Database`.
    5.  `Database` responds:
        *   If a review is not found (it's unique):
            1.  `BusinessLogic` instructs `Database` to insert the new review.
            2.  `Database` saves the review (initially pending validation).
            3.  `BusinessLogic` informs `Presentation`, which returns a `201 Created` (Review pending validation) with the Review ID to the `User`.
        *   If an identical review already exists, `BusinessLogic` informs `Presentation`, which returns a `409 Conflict` to the `User`.
*   **Key Steps - Admin Validating a Review**:
    1.  `User` (acting as Admin) sends a `POST /reviews/validate` request with the `reviewID` and validation status to `Presentation`.
    2.  `Presentation` forwards the request to `BusinessLogic`.
    3.  `BusinessLogic` instructs `Database` to update the review's status to "validated".
    4.  `Database` attempts to update the review:
        *   If the `reviewID` is not found, it returns an error to `BusinessLogic`, which results in a `404 Not Found` to the `User`.
        *   If the review is found and updated successfully, `Database` returns success to `BusinessLogic`.
    5.  `BusinessLogic` informs `Presentation`, which returns a `200 OK` (Review successfully validated) to the `User`.

## Authors
- [Clément Gibot](https://github.com/clementgibot25)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Badge](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/clementgibot25)
- [Arnaud Tilawat](https://github.com/TilawatArnaud)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Badge](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/TilawatArnaud)
- [Maxime Naguet](https://github.com/Roupies)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Badge](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/Roupies)