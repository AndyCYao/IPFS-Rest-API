# ZeroBit Take Home Question
Develop an API endpoint that allows for the updating of IPFS files.

## Goals of project:
1. Demonstrate an understanding of RESTful design and development.
2. Have solid knowledge of software development best practices e.g testing, documentation.
3. Can navigate obstacles efficiently and can traverse the stack.

## Project requirements:
Develop and deploy a simply restful API on top of IPFS.

This project will not require deployment to a public server. You will deploy them locally either using docker or some other virtual environment.

#### Routes:
1. Route to addFile `baseurl/add`

Response should be JSON with the following structure:
```
{
  "success": true,
  "error": "",
  "fileUrl": "<baseurl/filehash>",
  "fileHash": "<filehash>"
}
```

2. Route to deleteFile `baseurl/delete`
```
{
  "success": true,
  "error": ""
}
```

#### Documentation:
We want to see public facing documentation that others can use to easily understand the parameters of the API.

#### Testing:
Before submitting the API, make sure that the code is tested. Consider the various forms of testing.

#### Authentication:
Review and implement a JWT authentication service. JWTs are common methods of authenticating API calls.
Implement an authentication service either directly into the API or as a separate service.

#### Security
- Consider how users will authenticate to the API?
- How will the system be secured?
- What are some flaws of the existing systems?

Pseudo-code these as comments into the appropriate locations within your code.
