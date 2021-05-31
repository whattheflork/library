# Library Program

## Notes

At start time, ten books are inserted into the database as sample data to work with.

## Runbook

To install dependencies:

    pip install -r requirements.txt

To run the server:

    python src/server.py

## API Specs

GET localhost:5050/request

Query Parameters:

id : Book id to fetch request information for, if none is specified then fetches all books

Sample Response:

[
  {
      "available": "True",
      "id": 1,
      "timestamp": null,
      "title": "Gods of the Upper Air"
  },
  {
      "available": "True",
      "id": 2,
      "timestamp": null,
      "title": "Inherent Vice"
  }
]

POST localhost:5050/request

NOTE: Response returned is state of the book PRIOR to being requested - if the book is available
then all subsequent requests to fetch that book will reflect its unavailability

Sample Request:

{
  "email": "docsportello@test.com"
  "title": "Culture Warlords"
}

Sample Response:

{
  "available": "True",
  "id": 5,
  "timestamp": null,
  "title": "Culture Warlords"
}

Error Responses:

400 - Email is Invalid
404 - Title is not found

DELETE localhost:5050/request

Query Parameters:

id : Book id to delete request for

Sample Response:

[]

Error Responses:

400 - No id specfied
