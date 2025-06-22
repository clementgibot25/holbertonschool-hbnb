---
config:
  theme: neo-dark
---
sequenceDiagram
  participant User as User
  participant Presentation as Presentation
  participant BusinessLogic as BusinessLogic
  participant Database as Database
  User ->> Presentation: GET /amenities
  Presentation ->> BusinessLogic: List Amenities
  BusinessLogic ->> Database: Retrieve All Amenities
  Database -->> BusinessLogic: Return Amenities List (e.g., [wifi, pool, parking])
  BusinessLogic -->> Presentation: Send Amenities List
  Presentation -->> User: Return 200 OK (Amenities List)
  User ->> Presentation: POST /places (title, description, price, latitude, longitude, list[amenities])
  Presentation ->> Presentation: Validate Format
  alt Invalid Input Data (400)
    Presentation -->> User: Return 400 Bad Request (Validation Error)
  else Place Already Exists (409)
    Presentation ->> BusinessLogic: Submit Place Data
    BusinessLogic ->> Database: Query Place Existence (title, latitude, longitude)
    Database -->> BusinessLogic: Place found (e. g. ID: 456)
    BusinessLogic -->> Presentation: Return 409 Conflict<br>(Place Already Exists)
    Presentation -->> User: Return 409 Conflict
  else Place Created Successfully (201)
    Presentation ->> BusinessLogic: Submit Place Data
    BusinessLogic ->> Database: Query Place Existence (title, latitude, longitude)
    Database -->> BusinessLogic: Place not found
    BusinessLogic ->> Database: Insert new Place (data)
    Database -->> BusinessLogic: Success (Place ID: 123)
    BusinessLogic -->> Presentation: Return 201 Created (Place ID: 123)
    Presentation -->> User: Return 201 Created (Place ID: 123)
  else Internal Server Error (500)
    BusinessLogic ->> Database: (Any operation, e.g., Insert new Place)
    Database -->> BusinessLogic: Error
    BusinessLogic -->> Presentation: Return 500 Internal Server Error
    Presentation -->> User: Return 500 Internal Server Error
  end
