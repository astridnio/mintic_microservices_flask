from Models.Student import Student

class ControllerStudent():
    def __int__(self):
        print("Created ControllerStudent")

    # Function that calls all student list with their propierties
    def index(self):
        print("list all Students")
        anStudent={
            "_id":"abc123",
            "dni":"123",
            "name":"Holly",
            "lastname":"Stark"
        }
        return [anStudent]
    # Function to create Student Object
    def create(self,infoStudent):
        print("Create Student")
        theStudent = Student(infoStudent)
        return theStudent.__dict__

    # Display Student by Id
    def show(self,id):
        print("Display Student with id: ", id)
        theStudent = {
            "_id": id,
            "dni": "123",
            "name": "Holly",
            "lastname": "Stark"
        }
        return theStudent

    # Function to update an Student
    def update(self,id,infoStudent):
        print("Update Student with id: ", id)
        theStudent = Student(infoStudent)
        return theStudent.__dict__

    #Function to delete an Student
    def delete(self, id):
        print("Deleting Student with id", id)
        return{"deleted count": 1}