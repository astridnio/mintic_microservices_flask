from Models.Course import Course
from Models.Department import Department
from Repositories.RepositoryCourse import RepositoryCourse
from Repositories.RepositoryDepartment import RepositoryDepartment


class ControllerCourse():
    def __init__(self):
        self.repositoryCourse = RepositoryCourse()
        self.repositoryDepartment = RepositoryDepartment()

    def index(self):
        return self.repositoryCourse.findAll()

    def create(self, infoCourse):
        newCourse = Course(infoCourse)
        return self.repositoryCourse.save(newCourse)

    def show(self, id):
        theCourse = Course(self.repositoryCourse.findById(id))
        return theCourse.__dict__

    def update(self, id, infoCourse):
        currentCourse = Course(self.repositoryCourse.findById(id))
        currentCourse.name = infoCourse["name"]
        currentCourse.credits = infoCourse["credits"]
        return self.repositoryCourse.save(currentCourse)

    def delete(self, id):
        return self.repositoryCourse.delete(id)

    """ Department and Course dependency (1:N) """

    def assingDepartment(self, id, id_department):
        currentCourse = Course(self.repositoryCourse.findById(id))
        currentDepartment = Department(self.repositoryDepartment.findById(id_department))
        currentCourse.department = currentDepartment
        return self.repositoryCourse.save(currentCourse)