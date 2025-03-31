from sqlalchemy import text
from app import create_app, db
from app.models import User, Amenity
import os

app = create_app()

with app.app_context():
    if not os.path.exists('development.db'):
        with open('./app/persistence/db.sql', 'r') as file:
            script = file.read()
        try:
            with db.engine.connect() as conn:
                for statement in script.split(";"):
                    if statement.strip():
                        conn.execute(text(statement))
                        conn.commit()
        except Exception as e:
            print(f"Error executing script: {e}")

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
            new_amenity = Amenity(name=name)
            db.session.add(new_amenity)

    db.session.commit()