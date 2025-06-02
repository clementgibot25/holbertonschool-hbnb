---
config:
  theme: neo-dark
---
sequenceDiagram
  participant User as User
  participant Presentation as Presentation
  participant BusinessLogic as BusinessLogic
  participant Database as Database
  User ->> Presentation: POST Create Review<br>/reviews (username, review_text, place, date)
  Presentation ->> Presentation: Validate input (text length & date not in future)
  alt Invalid input
    Presentation -->> User: Return 400 Bad Request (Invalid review text or date)
  else Input valid
    Presentation ->> BusinessLogic: Check review existence (place, date, username)
    BusinessLogic ->> Database: Query review (same place, date, user)
    alt Review not found
      BusinessLogic ->> Database: Insert new review
      Database -->> BusinessLogic: Success (reviewID: 123)
      BusinessLogic -->> Presentation: Return 201 Created (Review pending validation)
      Presentation -->> User: Return 201 Created (reviewID: 123)
    else Review already exists
      Database -->> BusinessLogic: Review found
      BusinessLogic -->> Presentation: Return 409 Conflict (Review already exists)
      Presentation -->> User: Return 409 Conflict (Review already exists)
    end
  end
  User ->> Presentation: POST Admin Validate Review<br>/reviews/validate (reviewID: 123, validate)
  Presentation ->> BusinessLogic: Validate review (reviewID: 123)
  BusinessLogic ->> Database: Update review status to "validated"
  alt ReviewID not found
    Database -->> BusinessLogic: Not Found
    BusinessLogic -->> Presentation: Return 404 Not Found (Review not found)
    Presentation -->> User: Return 404 Not Found
  else Review found and validated
    Database -->> BusinessLogic: Success
    BusinessLogic -->> Presentation: Return 200 OK (Review successfully validated)
    Presentation -->> User: Return 200 OK (Review validated)
  end
