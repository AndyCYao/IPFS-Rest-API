#### Introduction
This project allows users to upload files to the InterPlanetary File System (IPFS). JSON web tokens (JWT) are supported for the `add` and `delete` endpoints. Unit tests are included for the REST layer; consult the section below for instructions.

#### How to Run
Theres two ways to run the project
#### 1st Way
1. in the root folder, enter `docker-compose up`. This will run a Flask API container, and a IPFS daemon container 
#### 2nd Way
1. create a new python virtual environment
2. enter the rest folder, and install environment with
`pip install -r requirements.txt`
3. start the flask API layer with `python run.py`
4. start the IPFS daemon with `ipfs daemon`

#### Sample curl commands
A set of postman JSON commands can be found at 
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
in the `rest` folder there are unit tests for most endpoints. Begin testing with `python test.py`. Note `ipfs daemon` must be running to test the `add` and `delete` endpoint

#### Repo Organization
The REST api is created with `flask` framework. the key files are

`app.py` - creates a flask app set up with REST endpoints, includes a SQLite database based on the ORM model described in models

`models.py` - this creates an object relational model (ORM) for handling user information, token black list.

`resources.py` - this file stores the implementation detail of each endpoint. 

`run.py` - main enter point for the app

#### Other Notes
You can check if a file is uploaded by `ipfs cat content_base__address > result.png` to see if its correct.
