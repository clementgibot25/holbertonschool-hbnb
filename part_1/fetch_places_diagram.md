---
config:
  theme: neo-dark
---
sequenceDiagram
  participant User as User
  participant Presentation as Presentation
  participant BusinessLogic as BusinessLogic
  participant Database as Database
  User ->> Presentation: GET /place Search a place (criteria)
  Presentation ->> Presentation: Validate `search criteria` format (e.g., non-empty, valid type)
  alt Invalid search criteria format at Presentation layer
    Presentation -->> User: Return 400 Bad Request (Invalid search criteria format)
  else `search criteria` format valid
    Presentation ->> BusinessLogic: Validate search (criteria more than 0)
    alt Business Logic Validation Failed (criteria not > 0)
      BusinessLogic -->> Presentation: Return 400 Bad Request (Search criteria must be greater than 0)
      Presentation -->> User: Return 400 Bad Request (Search criteria must be greater than 0)
    else Business Logic Validation Passed
      BusinessLogic ->> Database: Fetch list of place by criteria
      alt Database access error (e.g., DB down, connection issue)
        Database -->> BusinessLogic: Error
        BusinessLogic -->> Presentation: Return 500 Internal Server Error (DB connection issue)
        Presentation -->> User: Return 500 Internal Server Error
      else Database accessible
        Database -->> BusinessLogic: List of place found (or empty list)
        alt No places found
          BusinessLogic -->> Presentation: Return 200 OK (Empty list)
          Presentation -->> User: Return 200 OK (No places found)
        else Places found
          BusinessLogic -->> Presentation: Return 200 OK (List of place found : ID : 123,456,789)
          Presentation -->> User: Return 200 OK (List of place found : ID : 123,456,789)
        end
      end
    end
  end
