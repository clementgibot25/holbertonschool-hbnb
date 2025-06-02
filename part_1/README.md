# Part 1: System Design Diagrams

This directory contains several diagrams illustrating the architecture and key processes of the HBNB project. These diagrams are created using Mermaid.js and describe the data model and interactions between different components of the system.

## Diagrams Overview

The following diagrams are included:

1.  **`business_logic_layer.md`**: A **Class Diagram** that outlines the main data models (entities) of the application, their attributes, methods, and relationships.
2.  **`fetch_places_diagram.md`**: A **Sequence Diagram** detailing the process of a user searching for and fetching a list of places.
3.  **`place_creation_diagram.md`**: A **Sequence Diagram** illustrating the workflow for a user creating a new place listing.
4.  **`register_user_diagram.md`**: A **Sequence Diagram** showing the steps involved in registering a new user.
5.  **`submit_review_diagram.md`**: A **Sequence Diagram** describing the process for a user submitting a review for a place and an administrator validating that review.

## Detailed Explanations

### 1. Business Logic Layer (`business_logic_layer.md`)

![Business Logic Layer](https://www.mermaidchart.com/raw/92cf6e30-8ccb-4114-826c-ec5e7cfa489a?theme=dark&version=v0.1&format=svg)

This class diagram provides a high-level view of the core entities in the HBNB system.

*   **Purpose**: To define the structure of the data, including the properties of each entity and how they relate to one another.
*   **Key Entities**:
    *   `BaseModel`: An abstract base class providing common attributes like `Unique_ID`, `creation_time`, and `update_time`, along with basic CRUD methods (`create`, `update`, `delete`, `listed`).
    *   `User`: Represents a user of the system. Inherits from `BaseModel`. Attributes include `first_name`, `last_name`, `email`, `password` (private), `is_admin`, and `is_owner`. It has a `register()` method.
    *   `Place`: Represents a property listing. Inherits from `BaseModel`. Attributes include `title`, `description`, `price`, location details (`latitude`, `longitude`, `city`, `state`), and a list of `amenities`. Methods include `review_list()` and `get_average_rating()`.
    *   `Amenity`: Represents an amenity that a place can offer (e.g., Wi-Fi, pool). Inherits from `BaseModel`. Attributes include `name` and `description`.
    *   `Review`: Represents a review written by a user for a place. Inherits from `BaseModel`. Attributes include `rating`, `comment`, `author` (User), `for_place` (Place), and `approved` (private boolean). It has an `approved_by_admin()` method.
*   **Relationships**:
    *   `User`, `Place`, `Amenity`, and `Review` all inherit from `BaseModel`.
    *   A `User` can own zero or more `Place`s (one-to-many).
    *   A `Place` can offer zero or more `Amenity`s, and an `Amenity` can be offered by multiple `Place`s (many-to-many).
    *   A `User` can write zero or more `Review`s (one-to-many).
    *   A `Place` can have zero or more `Review`s (one-to-many).
*   **Notes**:
    *   `BaseModel` is abstract.
    *   Users can be regular users or administrators.
    *   Each Place is owned by one User.
    *   Reviews are linked to both a User (author) and a Place.

### 2. Fetch Places Diagram (`fetch_places_diagram.md`)

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

### 3. Place Creation Diagram (`place_creation_diagram.md`)

![Place Creation Diagram](https://www.mermaidchart.com/raw/4177e42c-0402-47d5-9683-81c4f0fb2347?theme=dark&version=v0.1&format=svg)

This sequence diagram details the process of a user creating a new place listing.

*   **Purpose**: To outline the steps involved from the user initiating the creation of a place to its persistence in the database.
*   **Actors**: `User`, `Presentation`, `BusinessLogic`, `Database`.
*   **Key Steps**:
    1.  (Optional Prerequisite) `User` may first request a list of available amenities via `GET /amenities`. This involves `Presentation` -> `BusinessLogic` -> `Database` and back to display options to the user.
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

### 4. Register User Diagram (`register_user_diagram.md`)

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

### 5. Submit Review Diagram (`submit_review_diagram.md`)

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

## How to View Diagrams

These diagrams are written in Mermaid.js syntax. You can view them:

*   By using a Markdown editor or previewer that supports Mermaid.js (e.g., VS Code with a Mermaid extension, GitLab, GitHub in some contexts).
*   By pasting the code into the [Mermaid Live Editor](https://mermaid.live).

Each `.md` file in this directory contains the Mermaid code for one diagram.
