from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve
from Controllers.ControllerStudent import ControllerStudent
from Controllers.ControllerCourse import ControllerCourse
from Controllers.ControllerDepartment import ControllerDepartment

app = Flask(__name__)
cors = CORS(app)


######################### Controllers init ##################################################
myControllerStudent = ControllerStudent()
myControllerCourse = ControllerCourse()
myControllerDepartment = ControllerDepartment()

############################## Init Test Route ##############################################
@app.route("/",methods=['GET'])
def test():
    json = {}
    json["message"]="Server running ..."
    return jsonify(json)
############################################################################

############################## Student Routes ##############################################
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
############################################################################

############################## Department Routes ##############################################
@app.route("/department",methods=['GET'])
def getDepartments():
    json = myControllerDepartment.index()
    return jsonify(json)

@app.route("/department",methods=['POST'])
def createDepartment():
    data = request.get_json()
    json = myControllerDepartment.create(data)
    return jsonify(json)

@app.route("/department/<string:id>",methods=['GET'])
def getDepartment(id):
    json = myControllerDepartment.show(id)
    return jsonify(json)

@app.route("/department/<string:id>",methods=['PUT'])
def updateDepartment(id):
    data = request.get_json()
    json = myControllerDepartment.update(id, data)
    return jsonify(json)

@app.route("/department/<string:id>",methods=['DELETE'])
def deleteDepartment(id):
    json = myControllerDepartment.delete(id)
    return jsonify(json)
############################################################################

############################## Course Routes ##############################################
@app.route("/course",methods=['GET'])
def getcourses():
    json = myControllerCourse.index()
    return jsonify(json)

@app.route("/course",methods=['POST'])
def createCourse():
    data = request.get_json()
    json = myControllerCourse.create(data)
    return jsonify(json)

@app.route("/course/<string:id>",methods=['GET'])
def getCourse(id):
    json = myControllerCourse.show(id)
    return jsonify(json)

@app.route("/course/<string:id>",methods=['PUT'])
def updateCourse(id):
    data = request.get_json()
    json = myControllerCourse.update(id, data)
    return jsonify(json)

@app.route("/course/<string:id>",methods=['DELETE'])
def deleteCourse(id):
    json = myControllerCourse.delete(id)
    return jsonify(json)
############################################################################

############################## Department - Course Routes ##############################################
@app.route("/course/<string:id>/department/<string:id_department>",methods=['PUT'])
def assingDepartmentCourse(id, id_department):
    json = myControllerCourse.assingDepartment(id, id_department)
    return jsonify(json)


############################################################################
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
