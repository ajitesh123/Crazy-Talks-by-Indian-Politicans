
# Motivation for project

This API is my attempt to keep a record of funny and crazy thing Indians politicians say. First, I believe existence of public repository might make politicians restrict what they say. Second, I see this project helping common person keep tab of crazt things said by politicians and help them accountable. At the least or most importantly (depends how you see it), this project will you get some fun out of Indian politics.

# Getting Started
### Virtual Environment Setup
Initialize and activate a virtualenv:

```
$ cd YOUR_PROJECT_DIRECTORY_PATH/
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

### Installing Dependencies

Use Pip to install all of the required packages we selected within the `requirements.txt` file.
```
$ pip install -r requirements.txt
```
### Tech Stack

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

# API Documentation

[Refer POSTMAN for API documentation] - https://web.postman.co/collections/8444799-1811f415-33c4-4417-85c7-dc57d349c96f

This flask based API will fetch you crazy things politicians talk.

No permission is required for GET request. POST request for creating a new question would require the "Creator" role's permission. Editing (PATCH) and deleting (DELETE) a question would require the "Admin" role's permissions.

### Getting Started
Base Url - At present, this application runs locally (htttp://127.0.0.1:5000/) and at Heroku (https://mock-final.herokuapp.com/).

### RBAC (Authorization)
No permission is required for GET request. This API used Auth0 for authentication and authorization.

#### Creater Role
POST request for creating a new quote would require the "Creator" role's permission.

#### Admin Role
Editing (PATCH) and deleting (DELETE) a quote would require the "Admin" role's permissions.

### Error Handling

Error are returned as JSON objects in the following formats:

```
{
  'success': False
  'error': 400,
  'message'; 'bad request'
}
```
The API could return following error:

400: Bad Request
- 404: Resource not found
- 422: Unprocessable
- 500: Internal server error

## Rate limit
There isn't a limit to the number of requests an user can send.

## Register to get adequate for permissions

Use this URL to register to get auth token: https://xupler.auth0.com/authorize?audience=quote&response_type=token&client_id=e25ZEQCe0drveyMSsv96ojqEKL4G2Q6f&redirect_uri=http://localhost:8080/login-results

To register as [Admin] use following details:
- [email]: admin@quote.com
- [password]: test@123

To register as [User] use following details:
- [email]: creator@quote.com
- [password]: test@123

## User
As a user, you can make GET requests to fetch quotes, parties, and politicians. No authorization is required to make this request.


### POST: POST - Search Quotes
http://127.0.0.1:5000/quotes/search
Fetches quotes that have the search term in their text. An exact match of the word is required to fetch results.

Headers
```
Content-Type	application/json
```

Bodyraw (application/json)
```
{
	"searchTerm": "Poverty"
}
```

Example RequestPOST - Search Quotes
```
curl --location --request POST 'http://127.0.0.1:5000/quotes/search' \
--header 'Content-Type: application/json' \
--data-raw '{
	"searchTerm": "Poverty"
}'
```

Example Response: 200 OK
```
{
  "current_quotes": [
    {
      "id": 1,
      "party_name": "Indian National Congress",
      "politician_name": "Rahul Gandhi",
      "text": "Poverty is just a state of mind. It does not mean the scarcity of food, money or material things. If one possesses self-confidence, then one can overcome poverty.",
      "topic": "Poverty"
    }
  ],
  "success": true,
  "total_quotes": 1
}
```

### GET: GET Quotes

http://127.0.0.1:5000/quotes
This endpoint fetches quotes in pagination form. You can specify the "page" in the URL as a parameter.

```
Request example: ' http://127.0.0.1:5000/quotes?page=2 '
```

The returned object included text, topic, party name, and politician name.

Example Request: GET Quotes
```
curl --location --request GET 'http://127.0.0.1:5000/quotes'
```

Example Response: 200 OK
```
{
    "quotes": [
        {
            "id": 1,
            "party_name": "Indian National Congress",
            "politician_name": "Rahul Gandhi",
            "text": "Poverty is just a state of mind. It does not mean the scarcity of food, money or material things. If one possesses self-confidence, then one can overcome poverty.",
            "topic": "Poverty"
        },
        {
            "id": 2,
            "party_name": "Indian National Congress",
            "politician_name": "Rahul Gandhi",
            "text": "We will stop 99% of the terror attacks but 1% of attacks might get through.",
            "topic": "Mumbai Serial Blast"
        },
        {
            "id": 3,
            "party_name": "Indian National Congress",
            "politician_name": "Rahul Gandhi",
            "text": "10 out of 7 youths in Punjab are hooked on to drugs.",
            "topic": "Punjab Drug Problem"
        },
        {
            "id": 4,
            "party_name": "Indian National Congress",
            "politician_name": "Rahul Gandhi",
            "text": "Today I got up in the night.",
            "topic": "UP Election"
        },
        {
            "id": 6,
            "party_name": "Indian National Congress",
            "politician_name": "Rahul Gandhi",
            "text": "Yahan Hindustan mein hamara jaat ka concept hai. Is mein bhi escape velocity chahiye. Dalit ko dharti pe Jupiter ki escape velocity chahiye",
            "topic": "UP Election"
        }
    ],
    "success": true,
    "total_quotes": 9
}
```

### GET: GET Political Parties

http://127.0.0.1:5000/parties
Fetches a list of political parties along with quotes by the politicians of these parties. You can specify the "page" in the URL as a parameter.

```
Request example: ' http://127.0.0.1:5000/parties?page=2 '
```

Example Request: GET Political Parties
```
curl --location --request GET 'http://127.0.0.1:5000/parties'
```

Example Response: 200 OK
```
{
    "parties": [
        {
            "count_politicians": 1,
            "count_quotes": 2,
            "name": "Bhartiya Janta Party (BJP)",
            "party_symbol": "https://upload.wikimedia.org/wikipedia/en/1/1e/Bharatiya_Janata_Party_logo.svg",
            "politicians": [
                "Narendra Modi"
            ],
            "quotes": [
                "We worship Lord Ganesha. There must have been some plastic surgeon at that time who got an elephant’s head on the body of a human being and began the practice of plastic surgery.",
                "Wah kya girlfriend hai. Apne kabhi dekha hai 50 crore ka girlfriend?"
            ]
        },
        {
            "count_politicians": 1,
            "count_quotes": 7,
            "name": "Indian National Congress",
            "party_symbol": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Flag_of_the_Indian_National_Congress.svg/1200px-Flag_of_the_Indian_National_Congress.svg.png",
            "politicians": [
                "Rahul Gandhi"
            ],
            "quotes": [
                "Poverty is just a state of mind. It does not mean the scarcity of food, money or material things. If one possesses self-confidence, then one can overcome poverty.",
                "We will stop 99% of the terror attacks but 1% of attacks might get through.",
                "10 out of 7 youths in Punjab are hooked on to drugs.",
                "Today I got up in the night.",
                "Yahan Hindustan mein hamara jaat ka concept hai. Is mein bhi escape velocity chahiye. Dalit ko dharti pe Jupiter ki escape velocity chahiye",
                "People call us an elephant.. We are not an elephant.. we are a beehive.. it's funny but think about it. Which is more powerful? an elephant or a beehive?",
                "Aisi machine lagaunga, iss side se aaloo ghusega, uss side se sona niklega."
            ]
        }
    ],
    "success": true,
    "total_parties": 3
}
```
### GET: GET Politicians

http://127.0.0.1:5000/politicians
Fetches a list of politicians with the names of their parties and quotes. You can specify the "page" in the URL as a parameter.

```
Request example: ' http://127.0.0.1:5000/politicians?page=2 '
```

Example Request: GET Politicians
```
curl --location --request GET 'http://127.0.0.1:5000/politicians'
```

Example Response: 200 OK
```
{
    "politicians": [
        {
            "count_quotes": 2,
            "famous_posts": "Prime Minister of India",
            "image_link": null,
            "name": "Narendra Modi",
            "party_name": "Bhartiya Janta Party (BJP)",
            "quotes": [
                "We worship Lord Ganesha. There must have been some plastic surgeon at that time who got an elephant’s head on the body of a human being and began the practice of plastic surgery.",
                "Wah kya girlfriend hai. Apne kabhi dekha hai 50 crore ka girlfriend?"
            ]
        },
        {
            "count_quotes": 7,
            "famous_posts": "President of Congress",
            "image_link": null,
            "name": "Rahul Gandhi",
            "party_name": "Indian National Congress",
            "quotes": [
                "Poverty is just a state of mind. It does not mean the scarcity of food, money or material things. If one possesses self-confidence, then one can overcome poverty.",
                "We will stop 99% of the terror attacks but 1% of attacks might get through.",
                "10 out of 7 youths in Punjab are hooked on to drugs.",
                "Today I got up in the night.",
                "Yahan Hindustan mein hamara jaat ka concept hai. Is mein bhi escape velocity chahiye. Dalit ko dharti pe Jupiter ki escape velocity chahiye",
                "People call us an elephant.. We are not an elephant.. we are a beehive.. it's funny but think about it. Which is more powerful? an elephant or a beehive?",
                "Aisi machine lagaunga, iss side se aaloo ghusega, uss side se sona niklega."
            ]
        }
    ],
    "success": true,
    "total_politicians": 3
}
```

## Creator
"Creator" role gives you the authority to add new quotes.

In order to make the following calls, your request must include "bearer token" with appropriate permissions in the authorization header.

### POST: POST - Create Quote

http://127.0.0.1:5000/quotes
Adds a new quote to the repository.

Headers
```
Content-Type	application/json
```

Bodyraw (application/json)
```
{
    "text": "People call us an elephant.. We are not an elephant.. we are a beehive.. it's funny but think about it. Which is more powerful? an elephant or a beehive?",
    "topic": "Gujrat Election",
    "party_id": 2,
    "politician_id": 2
}
```

Example Request: POST - Create Quote
```
curl --location --request POST 'http://127.0.0.1:5000/quotes' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text": "Congress is a 125 year old lady",
    "topic": "Gujrat Election",
    "party_id": 2,
    "politician_id": 2
}'
```

Example Response: 200 OK
```
{
    "quote": [
        {
            "id": 12,
            "party_name": "Indian National Congress",
            "politician_name": "Rahul Gandhi",
            "text": "Congress is a 125 year old lady",
            "topic": "Gujrat Election"
        }
    ],
    "success": true
}
```

### POST: POST - Easy create option for Quotes

http://127.0.0.1:5000/quick/quotes
Adds a new quote to the repository in an easy way. Instead of sending "party_id" and "politician_id", you just send the search terms that can uniquely identify party and politician.

A search term that results in either no result or more than one request would result in an error (400).

Headers
```
Content-Type	application/json
```

Bodyraw (application/json)
```
{
	"party": "Janta",
	"politician": "Modi",
	"text": "Wah kya girlfriend hai. Apne kabhi dekha hai 50 crore ka girlfriend?",
	"topic": "Himachal Pradesh Election"
}
```

Example Request: POST - Easy create option for Quotes
```
curl --location --request POST 'http://127.0.0.1:5000/quick/quotes' \
--header 'Content-Type: application/json' \
--data-raw '{
	"party": "Janta",
	"politician": "Modi",
	"text": "Wah kya girlfriend hai. Apne kabhi dekha hai 50 crore ka girlfriend?",
	"topic": "Himachal Pradesh Election"
}'
```

Example Response: 200 OK

```
{
    "quote": [
        {
            "id": 13,
            "party_name": "Bhartiya Janta Party (BJP)",
            "politician_name": "Narendra Modi",
            "text": "Wah kya girlfriend hai. Apne kabhi dekha hai 50 crore ka girlfriend?",
            "topic": "Himachal Pradesh Election"
        }
    ],
    "success": true
}
```

## Admin
"Admin" role gives you the authority to even delete and edit the quotes.

In order to make the following calls, your request must include "bearer token" with appropriate permissions in the authorization header.

### DELETE: DELETE - Delete a Quote

http://127.0.0.1:5000/quotes/8
This endpoint deletes a quote when provided with a quote ID.

Example Request: DELETE - Delete a Quote
```
curl --location --request DELETE 'http://127.0.0.1:5000/quotes/13'
```

Example Response: 200 OK
```
{
  "delete": 13,
  "success": true
}
```

### PATCH: PATCH - Change a Quote

http://127.0.0.1:5000/quotes/5
Make changes to the details of quotes based on new information provided.

Headers
```
Content-Type	application/json
```

Bodyraw (application/json)
```
{
	"text": "Aisi machine lagaunga, iss side se aaloo ghusega, uss side se sona niklega."
}
```

Example Request: PATCH - Change a Quote
```
curl --location --request PATCH 'http://127.0.0.1:5000/quotes/5' \
--header 'Content-Type: application/json' \
--data-raw '{
	"text": "Aisi machine lagaunga, iss side se aaloo ghusega, uss side se sona niklega."
}'
```

Example Response: 200 OK
```
{
    "quote": [
        {
            "id": 5,
            "party_name": "Indian National Congress",
            "politician_name": "Rahul Gandhi",
            "text": "Aisi machine lagaunga, iss side se aaloo ghusega, uss side se sona niklega.",
            "topic": "UP Election"
        }
    ],
    "success": true
}
```
