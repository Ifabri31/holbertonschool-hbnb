# *Project HBnB - Part 3 (Auth and DB)*

## 🧐 What is this part of the project about?
In part 3 of the HBnB project, you will extend the backend of the application by introducing user authentication, authorization and database integration using SQLAlchemy and SQLite for development. Later, you will configure MySQL for production environments. In this part, you will secure the backend, introduce persistent storage, and prepare the application for scalable real-world deployment.

## 📝 Objectives of the Project

- **Authentication and Authorization:** Implement JWT-based user authentication using Flask-JWT-Extended and role-based access control with the is_admin attribute for specific endpoints.
- **Database Integration:** Replace in-memory storage with SQLite for development using SQLAlchemy as the ORM and prepare for MySQL or other production grade RDBMS.
- **CRUD Operations with Database Persistence:** Refactor all CRUD operations to interact with a persistent database.
- **Database Design and Visualization:** Design the database schema using mermaid.js and ensure all relationships between entities are correctly mapped.
- **Data Consistency and Validation:** Ensure that data validation and constraints are properly enforced in the models.

## 🏗️ Project Structure

The structure of the project is as follows:

```
part3/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── amenities.py
│   │       ├── auth.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── users.py
│   ├── models/
│   │   ├── amenity.py
│   │   ├── basemodel.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── user.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── db.sql
│   │   ├── repository.py
│   │   └── user_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py
│   └── __init__.py
├── config.py
├── README.md
├── requirements.txt
├── run.py
└── test.py
```

## 👓 Diagrams

### Database Diagram

![Diagrama de Arquitectura](https://github.com/Ifabri31/holbertonschool-hbnb/blob/main/images/Diagrama%20Parte%203.png)

### *Importance of ER Diagrams in the Project*
The Entity-Relationship (ER) diagram is a crucial tool for visualizing the structure of the database, its tables, and how they are connected.
Since HBnB follows a relational database structure, defining one-to-many and many-to-many relationships will help ensure data integrity and query efficiency.

The provided schema includes five key tables, along with their attributes and relationships:

# Entities and Their Attributes

## 1. USER
**Description:** Represents the users of the platform, whether they are guests or hosts.  

**Attributes:**
- `id (PK)`: Unique identifier for the user.
- `first_name`: User's first name.
- `last_name`: User's last name.
- `email`: Email address (must be unique).
- `password`: User's password (stored securely).
- `is_admin`: Boolean indicating if the user is an administrator.

---

## 2. PLACE
**Description:** Represents an accommodation that can be booked.  

**Attributes:**
- `id (PK)`: Unique identifier for the place.
- `title`: Descriptive title of the place.
- `description`: Detailed description of the place.
- `price`: Price per night in dollars or the specified currency.
- `latitude`: Latitude of the place (geographic coordinate).
- `longitude`: Longitude of the place (geographic coordinate).
- `owner_id (FK)`: References `USER.id` (the owner of the place).

---

## 3. REVIEW
**Description:** Contains the reviews and ratings that users leave for places.  

**Attributes:**
- `id (PK)`: Unique identifier for the review.
- `text`: Content of the review.
- `rating`: User rating (e.g., from 1 to 5 stars).
- `user_id (FK)`: References `USER.id` (the user who wrote the review).
- `place_id (FK)`: References `PLACE.id` (the place being reviewed).

---

## 4. AMENITY
**Description:** List of features or additional services that a place can offer.  

**Attributes:**
- `id (PK)`: Unique identifier for the amenity.
- `name`: Name of the amenity (e.g., `"WiFi"`, `"Swimming Pool"`, `"Free Parking"`).

---

## 5. PLACE_AMENITY (Relation between Place and Amenity)
**Description:** This is a join table used to handle the many-to-many relationship between `PLACE` and `AMENITY`.  

**Attributes:**
- `place_id (FK)`: References `PLACE.id`.
- `amenity_id (FK)`: References `AMENITY.id`.

---

## 6. RESERVATION
**Description:** Represents a user's booking of a place.  

**Attributes:**
- `id (PK)`: Unique identifier for the reservation.
- `user_id (FK)`: References `USER.id` (the guest making the reservation).
- `place_id (FK)`: References `PLACE.id` (the reserved place).
- `check_in`: Check-in date.
- `check_out`: Check-out date.
- `status`: Reservation status (e.g., `"pending"`, `"confirmed"`, `"canceled"`).

---

## 🔗 Entity Relationships
The diagram shows how the entities interact with each other.  

### A `USER` can own multiple `PLACE`
- **One-to-many relationship** (`USER ||--o{ PLACE` → `"owns"`).  
- A user can own multiple places.

### A `USER` can write multiple `REVIEW`
- **One-to-many relationship** (`USER ||--o{ REVIEW` → `"writes"`).  
- A user can write multiple reviews, but each review belongs to a single user.

### A `PLACE` can receive multiple `REVIEW`
- **One-to-many relationship** (`PLACE ||--o{ REVIEW` → `"has"`).  
- A place can have many reviews, but each review is for a single place.

### A `USER` can make multiple `RESERVATION`
- **One-to-many relationship** (`USER ||--o{ RESERVATION` → `"books"`).  
- A user can book multiple places.

### A `PLACE` can appear in multiple `RESERVATION`
- **One-to-many relationship** (`PLACE ||--o{ RESERVATION` → `"reserved"`).  
- The same place can be booked multiple times by different users.

### A `PLACE` can have multiple `AMENITY`, and an `AMENITY` can be in multiple `PLACE`
- **Many-to-many relationship** (`PLACE ||--o{ PLACE_AMENITY` and `AMENITY ||--o{ PLACE_AMENITY`).  
- To represent this relationship, the intermediate table `PLACE_AMENITY` is used.

---

## Database Management
The application uses **SQLAlchemy** as an **ORM** to manage the database. The data models are defined in the `app/models` directory and handle the creation and manipulation of tables.

---

## Persistence Layer

### `repository.py`
This file defines a **repository system** for handling database access in an abstract and reusable way.

#### **Abstract Repository Class (`Repository`)**
Defines an interface for repository implementations with the following abstract methods:

- `add(obj)`: Adds an object to the database.
- `get(obj_id)`: Retrieves an object by its ID.
- `get_all()`: Retrieves all objects in the table.
- `update(obj_id, data)`: Updates an object identified by `obj_id` with the values in `data`.
- `delete(obj_id)`: Deletes an object by its ID.
- `get_by_attribute(attr_name, attr_value)`: Retrieves an object by a specific attribute.

#### **SQLAlchemy Repository (`SQLAlchemyRepository`)**
Implements the `Repository` interface using **SQLAlchemy**.

##### **Methods:**
``` python
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
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value)

    def get_one_or_more_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).all()
```

---

### `user_repository.py`
This file implements a specific repository for the `User` model, extending `SQLAlchemyRepository`.

#### **User Repository (`UserRepository`)**
Extends `SQLAlchemyRepository` to handle users.

##### **Methods:**
``` python
class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
```

---

## Database Schema (`db.sql`) (Incomplete)
This file contains the **SQL definition** for the `User` table.

### **User Table**
| Column     | Type          | Constraints |
|------------|--------------|-------------|
| `id`       | CHAR(36)      | PRIMARY KEY |
| `first_name` | VARCHAR(255) | - |
| `last_name` | VARCHAR(255) | - |
| `email`    | VARCHAR(255)  | UNIQUE, NOT NULL |
| `password` | VARCHAR(255)  | NOT NULL (hashed) |
| `is_admin` | BOOLEAN       | DEFAULT FALSE |

#### **SQL Table Definition**
``` sql
CREATE TABLE IF NOT EXISTS User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);
```

---

## Authentication System
The authentication is managed using **JWT (JSON Web Tokens)** with the `flask-jwt-extended` extension.

### **Main Functionalities**
- **Login endpoint (`/login`)**: Validates credentials and generates a JWT token.
- **Protected endpoint (`/protected`)**: Only allows access to authenticated users.

### **Key Imports**
```python
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, current_user
from app import bcrypt
from app.services import facade
```

### **Login Model for API Requests**
```python
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})
```

### **Login Endpoint (`/login`)**
```python
@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        credentials = api.payload
        user = facade.get_user_by_email(credentials['email'])
        
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401
        
        access_token = create_access_token(identity=str(user.id), additional_claims={"is_admin": user.is_admin})
        return {'access_token': access_token}, 200
```

### **Protected Endpoint (`/protected`)**
```python
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        return {'message': f'Hello, user {current_user}'}, 200
```

---

## Authentication Flow Summary
1. **User logs in (`POST /auth/login`)**
   - Sends `email` and `password`.
   - Validates credentials.
   - Generates a JWT token and returns it to the client.
2. **Client uses the token for future requests**
   - Includes `Authorization: Bearer <TOKEN_JWT>` in headers.
   - If the token is valid, access is granted.
   - If the token is invalid or expired, a `401 Unauthorized` response is returned.

## 😎 Authors

* **[Franco Reyes](https://github.com/Franco-byte)**
* **[Fabrizzio Oviedo](https://github.com/Ifabri31)**
* **[Jonathan Pérez](https://github.com/Jonatha32)**
