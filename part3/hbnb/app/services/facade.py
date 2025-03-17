from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository #InMemoryRepository
from app.persistence.user_repository import UserRepository


class HBnBFacade:
    def __init__(self):
        self.user_repository = SQLAlchemyRepository(User)
        self.place_repository = SQLAlchemyRepository(Place)
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = SQLAlchemyRepository(Amenity)
        self.user_repo = UserRepository
        # self.user_repository = InMemoryRepository()
        # self.place_repository = InMemoryRepository()
        # self.review_repository = InMemoryRepository()
        # self.amenity_repository = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repository.add(user)
        return user        
    
    def get_user(self, user_id):
        return self.user_repository.get(user_id)
    
    def get_user_by_email(self, email):
        return self.user_repository.get_by_attribute('email', email)
    
    def get_all_users(self):
        user_list = []
        exclude = ['created_at', 'updated_at', 'is_admin', 'places', 'reviews', 'password']
        for obj in self.user_repository.get_all():
            filtered_dict = {}
            for key, value in vars(obj).items():
                if key not in exclude:
                    filtered_dict[key] = value
            user_list.append(filtered_dict)
        return user_list

    def update_user(self, user_id, data):
        return self.user_repository.update(user_id, data)
# _____________________________________________________________________________            
            
    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repository.add(place)
        return place
    
    def get_place(self, place_id):
        return self.place_repository.get(place_id)
    
    def get_all_places(self):
        places_list = []
        exclude = ['description', 'owner', 'review', 'amenities', 'created_at', 'updated_at']
        for obj in self.place_repository.get_all():
            filtered_dict = {}
            for key, value in vars(obj).items():
                if key not in exclude:
                    filtered_dict[key] = value
            places_list.append(filtered_dict)
        return places_list

    def update_place(self, place_id, place_data):
        place = self.place_repository.get(place_id)
        if place:
            place.update(place_data)
#_______________________________________________________________________________

    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repository.add(review)
        return review
    
    #todo: preguntar a nachos...
    def get_all_reviews(self):
        review_list = []
        exclude = ['place_id', 'user_id', 'created_at', 'updated_at']
        for obj in self.review_repository.get_all():
            filter_dict = {}
            for key, value in vars(obj).items():
                if key not in exclude:
                    filter_dict[key] = value
            review_list.append(filter_dict)
        return review_list
    
    def get_reviews_by_place(self, place_id):
        return self.review_repository.get_one_or_more_by_attribute('place_id', place_id)
    
    def get_review(self, review_id):
        return self.review_repository.get(review_id)
    
    def update_review(self, review_id, review_data):
        review = self.review_repository.get(review_id)
        if review:
            review.update(review_data)
    
    def delete_reviews(self, review_id):
        return self.review_repository.delete(review_id)
    
    def get_review_by_user_id(self, user_id):
        return self.review_repository.get_one_or_more_by_attribute('user_id', user_id)
#________________________________________________________________________________

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repository.add(amenity)
        return amenity
    
    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)
    
    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repository.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)

    def get_all_amenities(self):
        list_amenity = []
        for obj in self.amenity_repository.get_all():
            if isinstance(obj, Amenity):
                list_amenity.append(obj.name)
        return list_amenity


