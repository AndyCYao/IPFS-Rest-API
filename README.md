#### Introduction
This project allows users to upload files to the InterPlanetary File System (IPFS). JSON web tokens (JWT) are supported for the `add` and `delete` endpoints. Unit tests are included for the REST layer; consult the section below for instructions.

#### Activating the project
##### 1st Method
1. In the root folder, enter `docker-compose up`. This will run a Flask API container and an IPFS daemon container.
##### 2nd Method
1. Create a new python virtual environment.
2. Enter the rest folder, and install environment with
`pip install -r requirements.txt`.
3. Start the flask API layer with `python run.py`.
4. Start the IPFS daemon with `ipfs daemon`.

#### Sample curl commands
Postman JSON commands can be found at 
`IPFS Collections.postman_collection` in the main directory

```
// Register a new user, receive access token
curl -X POST \
  http://0.0.0.0:8081/registration \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "bob",
    "password": "hill"
}'

// Upload a file - Requires JWT access_token
curl -X POST \
  http://0.0.0.0:8081/add \
  -H 'Cache-Control: no-cache' \
  -H 'content-type: multipart/form-data; 
  -H "Authorization: JWT <token here>"
  -F fileObj=File to upload

// Delete a file - Requires JWT access_token
curl -X POST \
  http://0.0.0.0:8081/delete \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H "Authorization: JWT <token here>"
  -d '{
	"file": "Content Base Address"
}'
```

#### Unit Tests
There are unit tests for most endpoints in the `rest` folder. Begin testing with `python test.py`. Note that `ipfs daemon` must be running to test the `add` and `delete` endpoints.

#### Repo Organization
The REST api is created with `flask` framework. the key files are:

`app.py` 
- creates a flask app set up with REST endpoints
- includes an SQLite database based on the ORM model described in models

`models.py` 
- creates an object relational model (ORM) for handling user information
- declares token black list model

`resources.py` 
- stores the implementation details of each endpoint. 

`run.py` 
- main entry point for the app

#### Other Notes
Check if a file has been uploaded correctly by running `ipfs cat content_base__address > result.png`.
