from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve
from Controllers.ControllerStudent import ControllerStudent

app = Flask(__name__)
cors = CORS(app)

myControllerStudent = ControllerStudent()

# root
@app.route("/",methods=['GET'])
def test():
    json = {}
    json["message"]="Server running ..."
    return jsonify(json)

#Student Methods
@app.route("/students",methods=['GET'])
def getStudents():
    json = myControllerStudent.index()
    return jsonify(json)

@app.route("/students",methods=['POST'])
def createStudent():
    data = request.get_json()
    json = myControllerStudent.create(data)
    return jsonify(json)

@app.route("/students/<string:id>",methods=['GET'])
def getStudent(id):
    json = myControllerStudent.show(id)
    return jsonify(json)

@app.route("/students/<string:id>",methods=['PUT'])
def updateStudent(id):
    data = request.get_json()
    json = myControllerStudent.update(id, data)
    return jsonify(json)

@app.route("/students/<string:id>",methods=['DELETE'])
def deleteStudent(id):
    json = myControllerStudent.delete(id)
    return jsonify(json)

#loads server config
def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

#init the server
if __name__== '__main__':
    dataConfig = loadFileConfig()
    print("Server Running: " + "http://" + dataConfig["url-backend"] + ":" + str(dataConfig["port"]))
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])
