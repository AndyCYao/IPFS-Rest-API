from flask import Flask, request as flask_request, Response, abort
import requests
import datetime
import json

app = Flask(__name__)
IPFS_BASE_URL =  "http://localhost:5001"
IPFS_API_VER  =  "api/v0"

@app.route('/')
def index():
    return 'Hello'

@app.route("/add", methods=['POST'])
def add():
    '''connects to /api/v0/add
    args [file] required
    ''' 
    data        = flask_request.get_json()
    sourceFile  = data["files"]
    files = {'files' : (sourceFile, open(sourceFile, 'rb'))}

    response = requests.post('{}/{}/add'.format(IPFS_BASE_URL, IPFS_API_VER),
                                                files=files)
    print(response)
    print(response.json())
    if(response.status_code == 200):
        responseJson = response.json()
        responseHash = responseJson["Hash"]
        # Response from IPFS
        payload = {
            "success": True,
            "error": 0,
            "fileUrl": "{}/{}".format(IPFS_BASE_URL, responseHash),
            "fileHash": responseHash
        }
        return Response(json.dumps(payload), status=200,mimetype='application/json')
    else:
        return abort(500)

@app.route("/delete", methods=['POST'])
def delete():
    '''connects to /api/v0/files/rm
    args [files] required
    since IPFS is permanent, this will unpin the file and call garbage collection
    ''' 
    data  = flask_request.get_json()
    file  = "/{}".format(data["files"])
    print(file)
    print('{}/{}/files/rm?arg={}'.format(IPFS_BASE_URL, IPFS_API_VER, file))
    response = requests.post('{}/{}/files/rm?arg={}'.format(IPFS_BASE_URL, IPFS_API_VER, file))
    print(response.status_code)
    print(response.json())
    if(response.status_code == 200):
        payload = {
            "success": True,
            "error": ""
        }
        return Response(json.dumps(payload), status=200, mimetype="application/json")
    else:
        return abort(500)

@app.errorhandler(500)
def internal_error(error):
    return json.dumps({"error": error})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081,debug=True)