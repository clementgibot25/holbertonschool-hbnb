---
config:
  theme: neo-dark
---
sequenceDiagram
  participant User as User
  participant Presentation as Presentation
  participant BusinessLogic as BusinessLogic
  participant Database as Database
  User ->> Presentation: POST (first_name, last_name, email<br>password)
  Presentation ->> Presentation: Validate User Registration Data
  alt Invalid data
    Presentation -->> User: Return 400 Bad Request ( Format Error)<br>
  else Email exists
    Presentation ->> BusinessLogic: Submit User Data
    BusinessLogic ->> Database: Check if email already exists
    Database -->> BusinessLogic: Email already exists
    BusinessLogic -->> Presentation: Return 409 Conflict (email exists)
    Presentation -->> User: Return 409 Conflict
  else User Created Successfully
    Presentation ->> BusinessLogic: Submit User Data
    BusinessLogic ->> Database: Check if email already exists
    Database -->> BusinessLogic: Email doesn't exist
    BusinessLogic ->> Database: Saving User
    Database -->> BusinessLogic: Success
    BusinessLogic -->> Presentation: Return 201 (user created)
    Presentation -->> User: Return 201
  else Internal Server Error
    BusinessLogic ->> Database: Saving User
    Database -->> BusinessLogic: Error
    BusinessLogic -->> Presentation: Return 500 Internal Server Error
    Presentation -->> User: Return 500 Internal Server Error
  end
