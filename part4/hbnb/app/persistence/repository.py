from abc import ABC, abstractmethod
from app import db  # Import db from app
from app.models import User, Place, Review, Amenity  # Import your models

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()
    
    def get_one_or_more_by_attribute(self, attr_name, attr_value):
        instans = getattr(self.model, attr_name)
        consult = self.model.query.filter(instans == attr_value)
        obj_list = consult.all()
        return obj_list

# class InMemoryRepository(Repository):
#     def __init__(self):
#         self._storage = {}

#     def add(self, obj):
#         self._storage[obj.id] = obj

#     def get(self, obj_id):
#         return self._storage.get(obj_id)
    
#     def get_all(self):
#         return list(self._storage.values())

#     def update(self, obj_id, data):
#         obj = self.get(obj_id)
#         if obj:
#             obj.update(data)

#     def delete(self, obj_id):
#         if obj_id in self._storage:
#             del self._storage[obj_id]

#     def get_one_or_more_by_attribute(self, attr_name, attr_value):
#         obj_list = []
#         for obj in self._storage.values():
#             if getattr(obj, attr_name) == attr_value:
#                 obj_list.append(obj)
#         return obj_list
    
#     def get_by_attribute(self, attr_name, attr_value):
#         return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)