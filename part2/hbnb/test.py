from app.models.user import User
from app.models.basemodel import BaseModel

def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="hola")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value
    print("User creation test passed!")

test_user_creation()


from app.models.place import Place
from app.models.user import User
from app.models.review import Review

def test_place_creation():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com", password="chau")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=owner)

    # Adding a review
    review = Review(comment="Great stay!", rating=5, place=place, user=owner)
    place.add_review(review)

    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].comment == "Great stay!"
    print("Place creation and relationship test passed!")
    print(place.reviews[0].comment)

test_place_creation()


from app.models.amenity import Amenity


def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    # Amenity.amenities.add_amenity(amenity)
    print("Amenity creation test passed!")
    
test_amenity_creation()

