import pymongo
import certifi
from bson import DBRef
from bson.objectid import ObjectId
from typing import TypeVar, Generic, List, get_origin, get_args
import json

T = TypeVar('T')


class InterfaseRepository(Generic[T]):

    def __int__(self):
        ca = certifi.where()
        dataConfig = self.loadFileConfig()
        client = pymongo.MongoClient(dataConfig["data-db-connection"], tlsCAFile=ca)
        self.dataBase=client[dataConfig["name-db"]]
        theClass = get_args(self.__org_bases__[0])
        self.collection=theClass[0].__name__.lower()

    def loadFileConfig(self):
        with open('config.json') as f:
            data = json.load(f)
        return data

    def save(self, item: T):
        theCollection = self.dataBase[self.collection]
        theId = ""
        item = self.transformRefs(item)
        if hasattr(item, "_id") and item._id != "":
            theId = item._id
            _id = ObjectId(theId)
            theCollection = self.dataBase[self.collection]
            delattr(item, "_id")
            item = item.__dict__
            updateItem = {"$set": item}
            x = theCollection.update_one({"_id": _id }, updateItem)
        else:
            _id = theCollection.insert_one(item.__dict__)
            theId = _id.inserted_id.__str__()

        x = theCollection.find_one({"_id": ObjectId(theId)})
        x["_id"] = x["_id"].__str__()
        return self.findById(theId)

    def findAll(self):
        theCollection = self.dataBase[self.collection]
        data = []
        for i in theCollection.find():
            i["_id"] = i["_id"].__str__()
            i = self.transformObjectIds(i)
            i = self.getValuesDBRef(i)
            data.append(i)
        return data

    def update(self, id, item: T):
        _id = ObjectId(id)
        theCollection = self.dataBase[self.collection]
        delattr(item, "_id")
        item = item.__dict__
        updateItem = {"$set": item}
        x = theCollection.update_one({"_id": _id}, updateItem)
        return {"updated_count": x.matched_count}

    def delete(self, id):
        theCollection = self.dataBase[self.collection]
        count = theCollection.delete_one({"_id": ObjectId(id)}).deleted_count
        return {"deleted_count": count}

    def finById(self, id):
        theCollection = self.dataBase[self.collection]
        i = theCollection.find_one({"_id": ObjectId(id)})
        i = self.getValuesDBRef(i)

        if i == None:
            i = {}
        else:
            i["_id"] = i["_id"].__str__()
            return i

    def query(self, theQuery):
        theCollection = self.dataBase[self.collection]
        data = []

        for i in theCollection.find(theQuery):
            i["_id"]= i["_id"].__str__()
            i = self.transfromObjectIds(i)
            i = self.getValuesDBRef(i)
            data.append(i)
        return data

    def queryAggregation(self, theQuery):
        theCollection = self.dataBase[self.collection]
        data = []
        for i in theCollection.aggregate(theQuery):
            i["_id"] = i["_id"].__str__()
            i = self.transformObjectIds(i)
            i = self.getValuesDBRef(i)
            data.append(i)
        return data

    def getValuesDBRef(self, i):
        keys = i.keys()
        for k in keys:
            if isinstance(i[k], DBRef):
                theCollection = self.dataBase[i[k].collection]
                value = theCollection.find_one({"_id" : ObjectId(i[k].id)})
                value["_id"] = value["_id"].__str__()
                i[k] = value
                i[k] = self.getValuesDBRef(i[k])
            elif isinstance(i[k], list) and len(i[k]) > 0:
                i[k] = self.getValuesDBRefFromList(i[k])
            elif isinstance(i[k] , dict):
                i[k] = self.getValuesDBRef(i[k])
        return i

    def getValuesDBRefFromList(self, theList):
        newList = []
        theCollection = self.dataBase[theList[0]._id.collection]
        for item in theList:
            value = theCollection.find_one({"_id": ObjectId(item.id)})
            value["_id"] = value["_id"].__str__()
            newList.append(value)
        return newList

    def transformObjectIds(self, i):
        for attribute in i.keys():
            if isinstance(i[attribute], ObjectId):
                i[attribute] = i[attribute].__str__()
            elif isinstance(i[attribute], list):
                i[attribute]= self.formatList(i[attribute])
            elif isinstance(i[attribute], dict):
                i[attribute] = self.transformObjectIds(i[attribute])
        return i

    def formatList(self, i):
        newList = []
        for item in i:
            if isinstance(item, ObjectId):
                newList.append(item.__str__())
        if len(newList) == 0:
            newList = i
        return newList

    def transformRefs(self, item):
        theDict = item.__dict__
        keys = list(theDict.keys())
        for k in keys:
            if theDict[k].__str__().count("object") == 1:
                newObject = self.ObjectToDVRef(getattr(item, k))
                setattr(item, k, newObject)
        return item

    def ObjectToDBRef(self, item: T):
        nameCollection = item.__class__.__name__.lower()
        return DBRef(nameCollection, ObjectId(item._id))

