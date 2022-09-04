from abc import ABCMeta

#Creates the constructor
class AbstractModel(metaclass=ABCMeta):
    def __init__(self, data):
        for key, val in data.items():
            setattr(self, key, val)
