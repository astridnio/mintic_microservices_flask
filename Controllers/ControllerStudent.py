from Models.Student import Student
from Repositories.RepositoryStudent import RepositoryStudent


class ControllerStudent():

    def __int__(self):
        print("Created ControllerStudent")
        self.RepositoryStudent = RepositoryStudent()

    # Function that calls all student list with their propierties
    def index(self):
        """
        print("list all Students")
        anStudent={
            "_id":"abc123",
            "dni":"123",
            "name":"Holly",
            "lastname":"Stark"
        }
        return [anStudent]"""
        return self.RepositoryStudent.findAll()

    # Function to create Student Object
    def create(self, infoStudent):
        """print("Crear un estudiante")
        theEstudiante = Student(infoEstudiante)
        return theEstudiante.__dict__"""
        newStudent = Student(infoStudent)
        return self.RepositoryStudent.save(newStudent)

    # Display Student by Id
    def show(self, id):
        """print("Display Student with id: ", id)
        theStudent = {
            "_id": id,
            "dni": "123",
            "name": "Holly",
            "lastname": "Stark"
        }
        return theStudent"""
        theStudent = Student(self.RepositoryStudent.finById(id))
        return theStudent.__dict__

    # Function to update an Student
    def update(self, id, infoStudent):
        """print("Update Student with id: ", id)
        theStudent = Student(infoStudent)
        return theStudent.__dict__"""
        currentStudent = Student(self.RepositoryStudent.finById(id))
        currentStudent.dni = infoStudent["dni"]
        currentStudent.name = infoStudent["name"]
        currentStudent.lastname = infoStudent["lastname"]
        return self.RepositoryStudent.save(currentStudent)

    #Function to delete an Student
    def delete(self, id):
        """print("Deleting Student with id", id)
        return{"deleted count": 1}"""
        return self.RepositoryStudent.delete(id)