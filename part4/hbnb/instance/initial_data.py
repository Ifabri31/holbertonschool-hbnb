from app import create_app, db
from app.models import User, Amenity
import uuid
import os

from part2.hbnb.app.api.v1 import amenities

app = create_app()

with app.app_context():

    if not os.path.exists('development.db'):
        with open('app/persistence/db.sql', 'r') as file:
            script = file.read()

        with db.engine.connect() as conn:
            conn.execute(script)

    admin_user = User.query.filter_by(email="admin@hbnb.io").first()
    if not admin_user:
        admin_user = User(
            first_name="Admin",
            last_name="HBnB",
            email="admin@hbnb.io",
            password="admin1234",  
            is_admin=True
        )
        db.session.add(admin_user)
    #todo: No se si funciona si las creo en un bucle    
    amenity_names = ["Wifi", "Swimming Pool", "Air Conditioning"]
    for name in amenity_names:
        amenity = Amenity.query.filter_by(name=name).first()
        if not amenity:
            new_amenity = Amenity(id=str(uuid.uuid4()), name=name)
            db.session.add(new_amenity)

    # amenities = [
    #     Amenity(id=str(uuid.uui4()), name="Wifi"),
    #     Amenity(id=str(uuid.uuid4()), name="Swimming Pool"),
    #     Amenity(id=str(uuid.uuid4()), name="Air Conditioning"),
    # ]

    db.session.commit()