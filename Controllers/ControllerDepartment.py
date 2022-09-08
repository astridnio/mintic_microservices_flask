from Models.Department import Department
from Repositories.RepositoryDepartment import RepositoryDepartment


class ControllerDepartment():
    def __init__(self):
        self.repositoryDepartment = RepositoryDepartment()

    def index(self):
        return self.repositoryDepartment.findAll()

    def create(self, infoDepartment):
        newDepartment = Department(infoDepartment)
        return self.repositoryDepartment.save(newDepartment)

    def show(self, id):
        theDepartment = Department(self.repositoryDepartment.findById(id))
        return theDepartment.__dict__

    def update(self, id, infoDepartment):
        currentDepartment = Department(self.repositoryDepartment.findById(id))
        currentDepartment.name = infoDepartment["name"]
        currentDepartment.description = infoDepartment["description"]
        return self.repositoryDepartment.save(currentDepartment)

    def delete(self, id):
        return self.repositoryDepartment.delete(id)
